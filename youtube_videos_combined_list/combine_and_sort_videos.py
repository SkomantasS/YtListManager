import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
channel_handles = os.getenv("CHANNEL_HANDLES").split(',')

# Directory containing the .txt files
INPUT_DIR = "./youtube_videos"  # Change this to the directory containing your .txt files

# Output file
OUTPUT_FILE = "youtube_videos_combined_list/combined_and_sorted_videos.txt"

def read_and_combine_files(input_dir,start_date='2000-01-01T00:00:00+00:00'):
    combined_data = []

    # Iterate over all .txt files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_dir, file_name)
            
            # Read the .txt file
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)  # Read as dictionary for 'ID' and 'PublishedAt'
                for row in reader:
                    if datetime.fromisoformat(row["PublishedAt"].replace("Z", "+00:00")) < datetime.fromisoformat(start_date):
                        pass
                    else:
                        combined_data.append({
                            "ID": row["ID"],
                            "PublishedAt": row["PublishedAt"]
                        })

    return combined_data

def sort_by_published_date(data):
    # Sort the combined data by 'PublishedAt' (convert to datetime for accurate sorting)
    return sorted(data, reverse=False, key=lambda x: datetime.fromisoformat(x["PublishedAt"].replace("Z", "+00:00")))

def save_to_file(sorted_data, output_file):
    # Save the sorted data to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "PublishedAt"])
        writer.writeheader()
        writer.writerows(sorted_data)

def main():
    # Step 1: Read and combine data from all .txt files
    combined_data = read_and_combine_files(INPUT_DIR,'2024-01-01T00:00:00+00:00')
    
    # Step 2: Sort the combined data by 'PublishedAt'
    sorted_data = sort_by_published_date(combined_data)
    
    # Step 3: Save the sorted data to a new file
    save_to_file(sorted_data, OUTPUT_FILE)
    print(f"Sorted data has been saved to '{OUTPUT_FILE}'.")

def check_channel_video_proportions():
    combined_data = []
    channel_videos = [0] * len(channel_handles)

    # Iterate over all .txt files in the input directory
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".txt"):
            file_path = os.path.join(INPUT_DIR, file_name)
            
            # Read the .txt file
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)  # Read as dictionary for 'ID' and 'PublishedAt'
                for row in reader:
                    if datetime.fromisoformat(row["PublishedAt"].replace("Z", "+00:00")) < datetime.fromisoformat('2024-01-01T00:00:00+00:00'):
                        pass
                    else:
                        channel_videos[channel_handles.index(file_name.replace("_YoutubeVideos.txt", ""))] += 1
                        combined_data.append({
                            "ID": row["ID"],
                            "PublishedAt": row["PublishedAt"]
                        })
    
    # Create a pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(channel_videos, labels=channel_handles, autopct='%1.1f%%', startangle=140)
    plt.title('Proportion of Videos per Channel')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart as an image file
    plt.show()

if __name__ == "__main__":
    # main()
    check_channel_video_proportions()
