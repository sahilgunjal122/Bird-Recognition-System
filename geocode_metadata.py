import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the metadata file
df = pd.read_csv("metadata.csv")

# Initialize geocoder
geolocator = Nominatim(user_agent="pakshi-bird-mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Geocode each location
df["location_obj"] = df["Location"].apply(geocode)
df["latitude"] = df["location_obj"].apply(lambda loc: loc.latitude if loc else None)
df["longitude"] = df["location_obj"].apply(lambda loc: loc.longitude if loc else None)

# Drop rows where geocoding failed
df = df.dropna(subset=["latitude", "longitude"])

# Save to new CSV
df.to_csv("geocoded_metadata.csv", index=False)
print("✅ Saved to geocoded_metadata.csv")
