#\!/usr/bin/env python3
"""Test script for cf-images tool"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path

def run_command(cmd):
    """Run a command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_help():
    """Test help command"""
    print("Testing help command...")
    code, stdout, stderr = run_command("python3 /tmp/cloudflare-images-tool/cf-images --help")
    assert code == 0, f"Help command failed: {stderr}"
    assert "Cloudflare Images CLI" in stdout, "Help text missing"
    print("✓ Help command works")

def test_upload_help():
    """Test upload help"""
    print("Testing upload help...")
    code, stdout, stderr = run_command("python3 /tmp/cloudflare-images-tool/cf-images upload --help")
    assert code == 0, f"Upload help failed: {stderr}"
    assert "--id" in stdout, "Upload help incomplete"
    print("✓ Upload help works")

def test_missing_env():
    """Test missing environment variables"""
    print("Testing missing environment variables...")
    # Create a test image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp.write(b'PNG test data')
        tmp_path = tmp.name
    
    # Clear env vars
    env = os.environ.copy()
    env.pop('CLOUDFLARE_ACCOUNT_ID', None)
    env.pop('CLOUDFLARE_API_TOKEN', None)
    
    result = subprocess.run(
        [sys.executable, "/tmp/cloudflare-images-tool/cf-images", "upload", tmp_path],
        capture_output=True,
        text=True,
        env=env
    )
    
    os.unlink(tmp_path)
    
    assert result.returncode == 1, "Should fail without env vars"
    assert "Missing required environment variables" in result.stderr, "Wrong error message"
    print("✓ Environment variable validation works")

def test_file_validation():
    """Test file validation"""
    print("Testing file validation...")
    
    # Set dummy env vars
    env = os.environ.copy()
    env['CLOUDFLARE_ACCOUNT_ID'] = 'dummy'
    env['CLOUDFLARE_API_TOKEN'] = 'dummy'
    
    # Test non-existent file
    result = subprocess.run(
        [sys.executable, "/tmp/cloudflare-images-tool/cf-images", "upload", "/tmp/nonexistent.png"],
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 1, "Should fail for non-existent file"
    assert "File not found" in result.stderr, "Wrong error for missing file"
    print("✓ File validation works")

def test_json_format():
    """Test JSON format option"""
    print("Testing JSON format...")
    code, stdout, stderr = run_command("python3 /tmp/cloudflare-images-tool/cf-images --help")
    assert "--format" in stdout, "Format option missing"
    print("✓ JSON format option available")

def main():
    """Run all tests"""
    print("Running cf-images tests...\n")
    
    tests = [
        test_help,
        test_upload_help,
        test_missing_env,
        test_file_validation,
        test_json_format
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            return 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            return 1
    
    print("\n✓ All tests passed\!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
