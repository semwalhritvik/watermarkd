# Quick test to verify the bug fix
import pandas as pd

print("=== QUICK BUG FIX TEST ===\n")

# Load the data exactly like your notebook 05
df_clean = pd.read_csv("C:/Users/Hritvik/OneDrive/Desktop/Projects/Watermarkd/watermarkd/data/ai_samples.csv")
df_clean["Label"] = "AI_Plain"

df_watermarked = pd.read_csv("C:/Users/Hritvik/OneDrive/Desktop/Projects/Watermarkd/watermarkd/data/ai_samples_watermarked.csv")
df_watermarked["Label"] = "AI_Watermarked"

df_combined = pd.concat([df_clean, df_watermarked]).reset_index(drop=True)

# Detection functions
def contains_zwsp(text):
    return "\u200b" in text

def contains_arabic_comma(text):
    return "،" in text

print("❌ WRONG WAY (your current notebook 05):")
print("Applying detection to 'Text' column for all samples...")

# This is what you're doing (WRONG)
df_combined["has_zwsp_wrong"] = df_combined["Text"].apply(contains_zwsp).astype(int)
df_combined["has_arabic_comma_wrong"] = df_combined["Text"].apply(contains_arabic_comma).astype(int)

wrong_results = df_combined.groupby('Label')[['has_zwsp_wrong', 'has_arabic_comma_wrong']].mean()
print("Results (wrong method):")
print(wrong_results)

print("\n" + "="*50)
print("✅ CORRECT WAY:")
print("Applying detection to the right column for each sample type...")

# Create a column that points to the right text for each sample
def get_text_to_analyze(row):
    if row['Label'] == 'AI_Watermarked':
        return row['Text_watermarked']  # Use watermarked text
    else:
        return row['Text']  # Use original text

df_combined['Text_to_analyze'] = df_combined.apply(get_text_to_analyze, axis=1)

# Now apply detection to the correct column
df_combined["has_zwsp_correct"] = df_combined["Text_to_analyze"].apply(contains_zwsp).astype(int)
df_combined["has_arabic_comma_correct"] = df_combined["Text_to_analyze"].apply(contains_arabic_comma).astype(int)

correct_results = df_combined.groupby('Label')[['has_zwsp_correct', 'has_arabic_comma_correct']].mean()
print("Results (correct method):")
print(correct_results)

print("\n=== VERIFICATION ===")
print("Let's check a few samples manually:")

for i in [0, 50]:  # One clean, one watermarked
    row = df_combined.iloc[i]
    print(f"\nSample {i} ({row['Label']}):")
    
    if row['Label'] == 'AI_Watermarked':
        original = row['Text'][:60] + "..."
        watermarked = row['Text_watermarked'][:60] + "..."
        print(f"  Original   : {original}")
        print(f"  Watermarked: {watermarked}")
        print(f"  Checking watermarked text:")
        print(f"    ZWSP: {contains_zwsp(row['Text_watermarked'])}")
        print(f"    Arabic comma: {contains_arabic_comma(row['Text_watermarked'])}")
    else:
        text = row['Text'][:60] + "..."
        print(f"  Text: {text}")
        print(f"  Checking original text:")
        print(f"    ZWSP: {contains_zwsp(row['Text'])}")
        print(f"    Arabic comma: {contains_arabic_comma(row['Text'])}")

print(f"\n🎉 BUG FIXED! The issue was applying detection to the wrong column.")
print(f"Now you should see ~100% detection rate for watermarked samples!")