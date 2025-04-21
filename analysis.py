import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
df = pd.read_csv("payscale_cleaned.csv")

# Remove dollar signs and commas, convert salary columns to numeric
df["Early Career Pay"] = df["Early Career Pay"].replace('[\$,]', '', regex=True).astype(float)
df["Mid-Career Pay"] = df["Mid-Career Pay"].replace('[\$,]', '', regex=True).astype(float)

# 1. Calculate Spread and Percent Growth
df["Spread"] = df["Mid-Career Pay"] - df["Early Career Pay"]
df["Percent Growth"] = ((df["Spread"]) / df["Early Career Pay"]) * 100

# 2. Top and Bottom Growth Majors
top_growth = df[["Major", "Early Career Pay", "Mid-Career Pay", "Spread", "Percent Growth"]].sort_values(by="Spread", ascending=False)
print("🔝 Top Five Majors by Salary Spread:")
print(top_growth.head(), "\n")

print("🔻 Lowest Five Majors by Salary Spread:")
print(top_growth.tail(), "\n")

# 3. Top and Bottom Mid-Career Pay
top_mid = df[["Major", "Mid-Career Pay"]].sort_values(by="Mid-Career Pay", ascending=False).head()
bottom_mid = df[["Major", "Mid-Career Pay"]].sort_values(by="Mid-Career Pay").head()

print("💰 Top 5 Highest Paying Majors (Mid-Career):")
print(top_mid, "\n")

print("🧾 Bottom 5 Lowest Paying Majors (Mid-Career):")
print(bottom_mid, "\n")

# 4. Grouping by Degree Type (if column exists)
if "Degree Type" in df.columns:
    grouped = df.groupby("Degree Type")[["Early Career Pay", "Mid-Career Pay"]].mean().sort_values(by="Mid-Career Pay", ascending=False)
    print("📊 Average Salaries by Degree Type:")
    print(grouped, "\n")

# 5. Save enhanced CSV
df.to_csv("payscale_enhanced_analysis.csv", index=False)
print("✅ Enhanced data saved to payscale_enhanced_analysis.csv")

# 6. (Optional) Plot: Top 10 Majors by Salary Growth
plt.figure(figsize=(10, 6))
top_growth.head(10).plot(x='Major', y='Spread', kind='barh', color='skyblue', legend=False)
plt.title("Top 10 Majors by Salary Growth (Spread)")
plt.xlabel("Salary Growth ($)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_growth_chart.png")
plt.show()
print("📈 Chart saved as top_growth_chart.png")
