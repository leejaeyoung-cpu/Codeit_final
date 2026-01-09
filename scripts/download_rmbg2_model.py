"""
Download RMBG-2.0 model from Hugging Face
This script will prompt for HF token if needed and download the model
"""
import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download, login

def download_rmbg2_model():
    """Download RMBG-2.0 model"""
    
    model_id = "briaai/RMBG-2.0"
    local_dir = Path("models/rmbg-2.0")
    
    print("=" * 70)
    print("RMBG-2.0 Model Downloader")
    print("=" * 70)
    print(f"\nModel: {model_id}")
    print(f"Download to: {local_dir.absolute()}\n")
    
    # Check if model already exists
    if local_dir.exists() and any(local_dir.iterdir()):
        print(f"⚠️  Model directory already exists: {local_dir}")
        response = input("Do you want to re-download? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Check for HF_TOKEN
    hf_token = os.environ.get("HF_TOKEN")
    
    if not hf_token:
        print("\n📝 Hugging Face Token Required")
        print("-" * 70)
        print("To download RMBG-2.0, you need a Hugging Face token.")
        print("\nSteps:")
        print("1. Go to: https://huggingface.co/settings/tokens")
        print("2. Create a new token (Type: Read)")
        print("3. Accept model license: https://huggingface.co/briaai/RMBG-2.0")
        print("-" * 70)
        
        hf_token = input("\nEnter your HF token (or press Enter to skip): ").strip()
        
        if not hf_token:
            print("\n❌ Token required. Exiting.")
            return False
    
    # Login to Hugging Face
    try:
        print("\n🔑 Logging in to Hugging Face...")
        login(token=hf_token, add_to_git_credential=False)
        print("✅ Login successful!")
    except Exception as e:
        print(f"\n❌ Login failed: {e}")
        print("\nMake sure:")
        print("  - Token is valid")
        print("  - You have accepted the model license")
        return False
    
    # Download model
    try:
        print(f"\n📥 Downloading RMBG-2.0 model...")
        print("This may take a while (~1.7GB)...")
        
        local_dir.parent.mkdir(parents=True, exist_ok=True)
        
        snapshot_download(
            repo_id=model_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,
            ignore_patterns=["*.md", "*.txt", ".gitattributes"]
        )
        
        print(f"\n✅ Model downloaded successfully!")
        print(f"📁 Location: {local_dir.absolute()}")
        print(f"💾 Size: ~1.7GB")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        print("\nPossible reasons:")
        print("  - Model access not granted")
        print("  - Network issues")
        print("  - Insufficient disk space")
        return False

if __name__ == "__main__":
    print("\n")
    success = download_rmbg2_model()
    
    if success:
        print("\n" + "=" * 70)
        print("Next Steps:")
        print("=" * 70)
        print("1. Update config.py to use local model:")
        print("   bg_removal_use_local_model: bool = True")
        print("\n2. Restart your server:")
        print("   uvicorn app.main:app --reload")
        print("\n3. Test the model:")
        print("   python scripts/test_rmbg2_quick.py")
        print("=" * 70)
    
    sys.exit(0 if success else 1)
