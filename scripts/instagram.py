import json
import datetime
import instaloader

# Create an instance of Instaloader

# Optionally, login to Instagram (required for private profiles)
# L.login('your_username', 'your_password')
L = instaloader.Instaloader()


# Counter to keep track of the number of posts downloaded


# Iterate over the profile's posts

def updatePosts():
    print('updating instagram posts')
    post_count = 0
    postdata = []
    last_updated = datetime.datetime.now()
    # Specify the profile you want to download posts from
    profile_name = 'bradithan_draws'

    # Load the profile
    profile = instaloader.Profile.from_username(L.context, profile_name)
    for post in profile.get_posts():
        # Check if the post is a carousel (has multiple slides)
        if post.typename == 'GraphSidecar':
            # Get the first slide of the carousel
            first_slide = next(post.get_sidecar_nodes(), None)  # Use next() to get the first item
            if first_slide:
                # Download the first slide (image or video)
                if first_slide.is_video:
                    # Download the video
                    L.download_video(first_slide, target=f"public/{post.shortcode}_first_slide")
                    postdata.append({
                        "static_url" : f"public/{post.shortcode}_first_slide", 
                        "instagram_url": f"https://instagram.com/p/{post.shortcode}"
                        })
                else:
                    # Download the image
                    L.download_pic(filename=f"public/{post.shortcode}_first_slide", url=first_slide.display_url, mtime=post.date_utc)
                    postdata.append({
                        "static_url" : f"public/{post.shortcode}_first_slide", 
                        "instagram_url": f"https://instagram.com/p/{post.shortcode}"
                        })

        else:
            # If it's not a carousel, download the post as usual
            L.download_post(post, target=f"public")
            postdata.append({
                "static_url" : f"public/{post.shortcode}_first_slide", 
                "instagram_url": f"https://instagram.com/p/{post.shortcode}"
                })


        # Increment the post count
        post_count += 1

        # Stop after downloading 5 posts
        if post_count >= 5:
            break

        posts = {
            "posts": postdata,
            "last_updated": last_updated.isoformat() 
        }

        with open("posts.json", "w") as f:
            json.dump(posts, f, indent=4)

updatePosts()