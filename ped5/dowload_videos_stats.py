def download_video_details(video_id: str, region_code: str) -> Optional[dict]:
    api_key = os.getenv("API_KEY")
    link = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet%2Cstatistics&key={api_key}"
    try:
        response = requests.get(link)
        if response.status_code != 200:
            return None
        body = json.loads(response.content.decode("utf-8"))
        if len(body["items"]) < 1:
            return None

        item_body = body["items"][0]
        snippet = item_body["snippet"]
        statistics = item_body["statistics"]

        title = snippet.get("title", "")
        thumbnail = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        description = snippet.get("description", "")
        channel_title = snippet.get("channelTitle", "")
        category_id = snippet.get("categoryId", "")
        published_time = snippet.get("publishedAt", "")
        tags = "|".join(snippet.get("tags", []))
        views = statistics.get("viewCount", 0)

        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
            ratings_disabled = False
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
            comments_disabled = False
        else:
            comments_disabled = True
            comment_count = 0
        return {
            "video_id": video_id,
            "title": title,
            "channel_title": channel_title,
            "category_id": category_id,
            "publish_time": published_time,
            "tags": tags,
            "views": views,
            "likes": likes,
            "dislikes": dislikes,
            "comment_count": comment_count,
            "thumbnail_link": thumbnail,
            "comments_disabled": comments_disabled,
            "ratings_disabled": ratings_disabled,
            "video_error_or_removed": False,
            "description": description
        }
    except Exception as e:
        traceback.print_exc()
        print(f"Error by getting video ({video_id}): {e}")
        return None
