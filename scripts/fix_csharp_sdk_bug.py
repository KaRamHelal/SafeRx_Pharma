#!/usr/bin/env python3
"""
Auto-applies post-generation fixes to Fern-generated C# SDK.

Run this after every `fern generate --group csharp-sdk --api drug-safety-csharp` command.

Fixes applied:
1. StringContent cloning bug (Fern SDK v2.20.5) — ObjectDisposedException on retry
2. Copies SaferxApi.Custom.props — NuGet metadata (PackageId=SafeRx, description, license, etc.)
3. Copies README.md — NuGet package readme

The Custom.props and README source files live in fern/apis/drug-safety-csharp/
and are NOT deleted by Fern regeneration. This script copies them into the
generated output directory where the csproj expects them.

Usage:
    python scripts/fix_csharp_sdk_bug.py                    # Apply all fixes
    python scripts/fix_csharp_sdk_bug.py --check            # Verify fix state
    python scripts/fix_csharp_sdk_bug.py --pharma-root PATH # Override SafeRx_Pharma path
"""

import re
import shutil
import sys
from pathlib import Path

# ============================================================================
# Path resolution
# ============================================================================

# This script lives in SafeRx_OCR/scripts/
# SafeRx_Pharma is expected at the same level as SafeRx_OCR
OCR_ROOT = Path(__file__).parent.parent
DEFAULT_PHARMA_ROOT = OCR_ROOT.parent / "SafeRx_Pharma"

# Parse --pharma-root override
pharma_root = DEFAULT_PHARMA_ROOT
for i, arg in enumerate(sys.argv):
    if arg == "--pharma-root" and i + 1 < len(sys.argv):
        pharma_root = Path(sys.argv[i + 1])

# Source files (survive regeneration — version-controlled)
SOURCE_DIR = pharma_root / "fern" / "apis" / "drug-safety-csharp"
CUSTOM_PROPS_SRC = SOURCE_DIR / "SaferxApi.Custom.props"
README_SRC = SOURCE_DIR / "NuGetREADME.md"

# Generated output (overwritten by each fern generate)
SDK_ROOT = pharma_root / "fern" / "generated" / "csharp-sdk"
RAW_CLIENT_PATH = SDK_ROOT / "src" / "SaferxApi" / "Core" / "RawClient.cs"
CUSTOM_PROPS_DST = SDK_ROOT / "src" / "SaferxApi" / "SaferxApi.Custom.props"
README_DST = SDK_ROOT / "README.md"

# ============================================================================
# StringContent bug fix (Fern SDK v2.20.5)
# ============================================================================

BUGGY_PATTERN = r"""            default:
                clonedRequest\.Content = request\.Content;
                break;"""

FIXED_PATTERN = r"""            default:
                // MANUAL FIX \(Fern SDK v2\.20\.5 bug\): Properly clone StringContent"""

FIXED_CODE = """            default:
                // MANUAL FIX (Fern SDK v2.20.5 bug): Properly clone StringContent to prevent ObjectDisposedException
                // Bug: When retry logic disposes cloned request, it also disposes shared StringContent reference
                // Fix: Create a new StringContent instance instead of reusing the reference
                if (request.Content is StringContent stringContent)
                {
                    // Read the original content as byte array
                    var originalContent = await stringContent.ReadAsByteArrayAsync().ConfigureAwait(false);

                    // Create new StringContent with the same data
                    var clonedContent = new StringContent(
                        System.Text.Encoding.UTF8.GetString(originalContent),
                        System.Text.Encoding.UTF8,
                        stringContent.Headers.ContentType?.MediaType ?? "application/json"
                    );

                    // Copy all headers from original
                    foreach (var header in stringContent.Headers)
                    {
                        clonedContent.Headers.TryAddWithoutValidation(header.Key, header.Value);
                    }

                    clonedRequest.Content = clonedContent;
                }
                else
                {
                    // For non-StringContent types, use original reference (safe for non-retryable content)
                    clonedRequest.Content = request.Content;
                }
                break;"""


def check_if_fixed(content: str) -> bool:
    return bool(re.search(FIXED_PATTERN, content, re.MULTILINE))


def check_if_buggy(content: str) -> bool:
    return bool(re.search(BUGGY_PATTERN, content, re.MULTILINE))


def apply_stringcontent_fix(content: str) -> str:
    fixed = re.sub(BUGGY_PATTERN, FIXED_CODE, content, flags=re.MULTILINE)
    if fixed == content:
        raise ValueError("Bug pattern not found — SDK may have changed")
    return fixed


# ============================================================================
# User-Agent header fix (SafeRx bot detector requires non-empty User-Agent)
# ============================================================================

CLIENT_PATH_RELATIVE = Path("src") / "SaferxApi" / "SaferxApiClient.cs"

UA_BUGGY = '{ "X-Fern-SDK-Version", Version.Current },'
UA_FIXED_MARKER = '{ "User-Agent",'

UA_FIXED_CODE = '{ "X-Fern-SDK-Version", Version.Current },\n                { "User-Agent", $"SafeRx-CSharp-SDK/{Version.Current}" },'


def apply_useragent_fix(sdk_root: Path) -> bool:
    """Add User-Agent header to SaferxApiClient platform headers."""
    client_path = sdk_root / CLIENT_PATH_RELATIVE
    if not client_path.exists():
        print(f"[WARNING] {client_path} not found — skipping User-Agent fix")
        return False
    content = client_path.read_text(encoding="utf-8")
    if UA_FIXED_MARKER in content:
        print("[OK] User-Agent header already present")
        return True
    if UA_BUGGY not in content:
        print("[WARN] User-Agent fix pattern not found — SDK generator may have changed")
        return False
    fixed = content.replace(UA_BUGGY, UA_FIXED_CODE, 1)
    client_path.write_text(fixed, encoding="utf-8")
    print("[OK] User-Agent header added to SaferxApiClient")
    return True


# ============================================================================
# File copy (Custom.props + README)
# ============================================================================

def copy_nuget_assets():
    """Copy Custom.props and README from source to generated directory."""
    copied = 0

    if CUSTOM_PROPS_SRC.exists():
        shutil.copy2(CUSTOM_PROPS_SRC, CUSTOM_PROPS_DST)
        print(f"[OK] SaferxApi.Custom.props copied to {CUSTOM_PROPS_DST.relative_to(pharma_root)}")
        copied += 1
    else:
        print(f"[WARNING] Source not found: {CUSTOM_PROPS_SRC}")

    if README_SRC.exists():
        shutil.copy2(README_SRC, README_DST)
        print(f"[OK] README.md copied to {README_DST.relative_to(pharma_root)}")
        copied += 1
    else:
        print(f"[WARNING] Source not found: {README_SRC}")

    return copied


# ============================================================================
# Main
# ============================================================================

def main():
    check_only = "--check" in sys.argv

    # Verify generated SDK exists
    if not RAW_CLIENT_PATH.exists():
        print(f"[ERROR] {RAW_CLIENT_PATH} not found")
        print("   Run: fern generate --group csharp-sdk --api drug-safety-csharp --force")
        sys.exit(1)

    content = RAW_CLIENT_PATH.read_text(encoding="utf-8")
    is_fixed = check_if_fixed(content)
    is_buggy = check_if_buggy(content)

    if check_only:
        # Check StringContent fix
        if is_fixed:
            print("[OK] StringContent fix applied")
        elif is_buggy:
            print("[FAIL] StringContent bug present — fix NOT applied")
        else:
            print("[WARN] StringContent — unknown state")

        # Check Custom.props
        if CUSTOM_PROPS_DST.exists():
            print("[OK] SaferxApi.Custom.props present")
        else:
            print("[FAIL] SaferxApi.Custom.props missing")

        # Check README
        if README_DST.exists():
            print("[OK] README.md present")
        else:
            print("[FAIL] README.md missing")

        all_ok = is_fixed and CUSTOM_PROPS_DST.exists() and README_DST.exists()
        sys.exit(0 if all_ok else 1)

    # --- Apply StringContent fix ---
    if is_fixed:
        print("[OK] StringContent fix already applied")
    elif is_buggy:
        try:
            fixed = apply_stringcontent_fix(content)
            RAW_CLIENT_PATH.write_text(fixed, encoding="utf-8")
            print("[OK] StringContent fix applied")
        except Exception as e:
            print(f"[ERROR] StringContent fix failed: {e}")
            sys.exit(1)
    else:
        print("[WARN] StringContent bug pattern not found — SDK generator may have been updated")
        print("   If Fern SDK >= v2.21, this bug may be fixed upstream. Continuing...")

    # --- Apply User-Agent fix ---
    apply_useragent_fix(SDK_ROOT)

    # --- Copy NuGet assets ---
    copy_nuget_assets()

    print("\n[DONE] All fixes applied. Ready to pack:")
    print(f"   dotnet pack {SDK_ROOT}/src/SaferxApi/SaferxApi.csproj -c Release -p:Version=X.Y.Z")


if __name__ == "__main__":
    main()
