import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for professional look
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['font.family'] = 'sans-serif'

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

def generate_pie_chart():
    # Data: Truth about "Good First Issues"
    labels = ['Actually Available\n& Actionable (18%)', 'Stale/Abandoned (35%)', 'Already Claimed (47%)']
    sizes = [18, 35, 47]
    colors = ['#2ea043', '#8b949e', '#d29922']
    explode = (0.1, 0, 0)  # explode 1st slice

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%1.0f%%', shadow=False, startangle=140)

    # Styling texts
    plt.setp(autotexts, size=14, weight="bold", color="white")
    plt.setp(texts, size=12)

    ax.set_title('The Reality of "Good First Issue" Labels', fontsize=18, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('assets/issue_stats_pie.png', dpi=300, transparent=True)
    plt.close()

def generate_bar_chart():
    # Data: Time comparison
    categories = ['Setup & Auth', 'Find Issue', 'Fork & Clone', 'Create PR']
    manual_times = [8, 15, 3, 5]  # ~31 mins total
    automated_times = [1, 2, 0.5, 0.5]  # ~4 mins total

    x = range(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting
    rects1 = ax.bar([i - width/2 for i in x], manual_times, width, label='Manual Workflow', color='#d73a49')
    rects2 = ax.bar([i + width/2 for i in x], automated_times, width, label='Open Contribute (Automated)', color='#2ea043')

    # Add labels and title
    ax.set_ylabel('Time (Minutes)', fontsize=14, weight='bold')
    ax.set_title('Time to First PR: Manual vs Automated', fontsize=18, weight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend()

    # Add value labels on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}m',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=11)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig('assets/time_saved_bar.png', dpi=300, transparent=True)
    plt.close()

if __name__ == '__main__':
    generate_pie_chart()
    generate_bar_chart()
    print("Charts successfully generated in assets/ directory.")
