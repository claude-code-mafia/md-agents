# Google Cloud Setup Guide for Google Maps CLI

Follow these steps to set up your Google Cloud account and enable the required APIs.

## Step 1: Create or Select a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click the project dropdown at the top of the page
4. Either:
   - Select an existing project, OR
   - Click "New Project" and create one (give it a name like "maps-cli")

## Step 2: Enable Billing

Google Maps APIs require billing to be enabled (though you get $200/month free usage):

1. In the left sidebar, click "Billing"
2. Follow the prompts to set up a billing account
3. Link your project to the billing account

## Step 3: Enable Required APIs

### Method 1: Quick Links (Recommended)

Click each link below and click "Enable" for your project:

1. [Geocoding API](https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com)
2. [Directions API](https://console.cloud.google.com/apis/library/directions-backend.googleapis.com)
3. [Distance Matrix API](https://console.cloud.google.com/apis/library/distance-matrix-backend.googleapis.com)
4. [Places API](https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
5. [Time Zone API](https://console.cloud.google.com/apis/library/timezone-backend.googleapis.com)
6. [Elevation API](https://console.cloud.google.com/apis/library/elevation-backend.googleapis.com)

### Method 2: Manual Navigation

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable each of these APIs:
   - **Geocoding API** - Converts addresses to coordinates
   - **Directions API** - Provides directions between locations
   - **Distance Matrix API** - Calculates travel distance and time
   - **Places API** - Search for places and get details
   - **Time Zone API** - Get timezone for coordinates
   - **Elevation API** - Get elevation data

## Step 4: Create an API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "API key"
3. Your API key will be created and displayed
4. **IMPORTANT**: Click "Edit API key" to secure it:
   - Give it a name like "Maps CLI Key"
   - Under "Application restrictions", you can leave it as "None" for CLI usage
   - Under "API restrictions":
     - Select "Restrict key"
     - Select these APIs:
       - Geocoding API
       - Directions API
       - Distance Matrix API
       - Places API
       - Time Zone API
       - Elevation API
   - Click "Save"

## Step 5: Copy Your API Key

1. Copy the API key from the credentials page
2. Keep this key secure - don't share it publicly

## Step 6: Configure the CLI

Run the setup script:
```bash
cd ~/Projects/tool-library/google-maps
./setup.sh
```

Or set the environment variable:
```bash
export GOOGLE_MAPS_API_KEY="your-api-key-here"

# To make it permanent, add to your shell profile:
echo 'export GOOGLE_MAPS_API_KEY="your-api-key-here"' >> ~/.bashrc
# or for zsh:
echo 'export GOOGLE_MAPS_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## Step 7: Test the CLI

```bash
# Test geocoding
google-maps geocode "Empire State Building, New York"

# Test place search
google-maps place-search "coffee" --near "San Francisco"
```

## Billing and Quotas

- **Free tier**: $200/month credit covers ~40,000 geocoding requests or ~40,000 directions requests
- **Pricing**: See [Google Maps Platform Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- **Monitor usage**: Check "APIs & Services" → "Dashboard" in Google Cloud Console

## Troubleshooting

### "This API key is not authorized to use this service"
- Make sure you've enabled all required APIs
- Check API key restrictions match the APIs you're using

### "You have exceeded your daily request quota"
- Check your quotas in "APIs & Services" → "Quotas"
- Consider upgrading your billing account

### "REQUEST_DENIED"
- Verify billing is enabled on your project
- Ensure the API key is correct

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** instead of hardcoding keys
3. **Restrict API keys** to specific APIs you're using
4. **Monitor usage** regularly in Google Cloud Console
5. **Set up billing alerts** to avoid unexpected charges