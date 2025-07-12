# Debug script to check watermark detection
import pandas as pd
import re

# Load the watermarked data
df_watermarked = pd.read_csv("C:/Users/Hritvik/OneDrive/Desktop/Projects/Watermarkd/watermarkd/data/ai_samples_watermarked.csv")

# Test watermark detection functions
def contains_zwsp(text):
    return "\u200b" in text

def contains_arabic_comma(text):
    return "،" in text

def contains_fullwidth_period(text):
    return "。" in text

def contains_right_quote(text):
    return "'" in text

# Debug: Check first few watermarked samples
print("=== DEBUGGING WATERMARK DETECTION ===\n")

for i in range(3):
    original = df_watermarked.iloc[i]["Text"]
    watermarked = df_watermarked.iloc[i]["Text_watermarked"]
    
    print(f"Sample {i+1}:")
    print(f"Original: {original[:100]}...")
    print(f"Watermarked: {watermarked[:100]}...")
    
    # Check each watermark type
    print(f"Contains ZWSP: {contains_zwsp(watermarked)}")
    print(f"Contains Arabic comma: {contains_arabic_comma(watermarked)}")
    print(f"Contains fullwidth period: {contains_fullwidth_period(watermarked)}")
    print(f"Contains right quote: {contains_right_quote(watermarked)}")
    
    # Show character-by-character comparison of first 50 chars
    print("\nCharacter codes comparison (first 50 chars):")
    print("Original  :", [ord(c) for c in original[:50]])
    print("Watermarked:", [ord(c) for c in watermarked[:50]])
    print("-" * 80)

# Overall statistics
print(f"\nOverall Detection Stats:")
print(f"Total watermarked samples: {len(df_watermarked)}")
print(f"ZWSP detected in: {df_watermarked['Text_watermarked'].apply(contains_zwsp).sum()} samples")
print(f"Arabic comma detected in: {df_watermarked['Text_watermarked'].apply(contains_arabic_comma).sum()} samples")
print(f"Fullwidth period detected in: {df_watermarked['Text_watermarked'].apply(contains_fullwidth_period).sum()} samples")
print(f"Right quote detected in: {df_watermarked['Text_watermarked'].apply(contains_right_quote).sum()} samples")

# Check if the watermarked column actually exists and has data
print(f"\nData integrity check:")
print(f"Watermarked column has null values: {df_watermarked['Text_watermarked'].isnull().sum()}")
print(f"Watermarked column equals original: {(df_watermarked['Text'] == df_watermarked['Text_watermarked']).sum()}")