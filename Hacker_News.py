import requests
import pandas as pd
import matplotlib.pyplot as plt



top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(top_stories_url)
if response.status_code == 200:
    top_story_ids = response.json()
else:
    print('Error')



story_details = []
for story_id in top_story_ids[:10]:  
    story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
    response = requests.get(story_url)
    if response.status_code == 200:
        story_details.append(response.json())
    else:
        print(f'Failed to fetch story details for story ID {story_id}')
df_stories = pd.DataFrame(story_details)
df_stories.to_csv('top_stories.csv', index=False)


comment_details = []
for story in story_details:
    if 'kids' in story:     
        for comment_id in story['kids'][:10]: 
            comment_url = f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json'
            response = requests.get(comment_url)
            
            if response.status_code == 200:
                comment_details.append(response.json())
            else:
                print(f'Failed to fetch comment details for comment ID {comment_id}')
df_comments = pd.DataFrame(comment_details)
df_comments.to_csv('top_comments.csv', index=False)


df_stories = pd.read_csv('top_stories.csv')
df_comments = pd.read_csv('top_comments.csv')
average_comments = df_stories['descendants'].mean()
print(f'Average number of comments per story: {average_comments}')
plt.hist(df_stories['descendants'].dropna(), bins=20)
plt.xlabel('Number of Comments')
plt.ylabel('Frequency')
plt.title('Distribution of Comments per Story')
plt.show()
print('dune')


