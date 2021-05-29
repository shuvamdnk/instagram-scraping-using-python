# Import the module
# !pip install instaloader
import instaloader
import datetime
from flask import Flask , render_template ,request ,session ,redirect ,Response

app = Flask(__name__)
# Create an instance of Instaloader class
bot = instaloader.Instaloader()



@app.route('/profile' , methods =["GET", "POST"])
def profile():
    try:
        global u
        u = ''
        if request.method == "POST":
            u = request.form.get("user")
            fil = open("user.txt", "a")
            fil.write(f"{u} => {datetime.datetime.now()} \n")
            fil.close()

        user = u


        if user == '':
            profile = instaloader.Profile.from_username(bot.context, "instagram")
        else:
            profile = instaloader.Profile.from_username(bot.context, user)


        username = profile.username
        total_posts = profile.mediacount
        followers = profile.followers
        following = profile.followees
        bio = profile.biography
        link = profile.external_url
        name = profile.full_name
        profile_pic = profile.profile_pic_url
        verified = profile.is_verified



        # posts objects
        posts = profile.get_posts()
        ft = []
        l = []
        tag = []
        caption = []
        like = []
        location = []
        comment = []
        i = 0

        # list appending
        for index, post in enumerate(posts, 1):
            if i < 10:
                if post.is_video == True:
                    l.append(post.video_url)
                    ft.append(1)
                    # print(post.video_url)
                else:
                    l.append(post.url)
                    ft.append(0)
                tag.append(post.tagged_users)
                caption.append(post.caption)
                like.append(post.likes)
                location.append(post.location)
                comment.append(post.comments)
                i += 1
            elif i == 10:
                break

        return render_template('profile.html', username=username,verified=verified, name=name, total_posts=total_posts, following=following,
                               followers=followers, bio=bio, link=link, profile_pic=profile_pic, details=zip(l,tag,caption,location,like,ft,comment) , u=u)

    except Exception as e:
        error = "An Error Occur!!"
        return render_template('error.html', err = e)



@app.route('/' , methods =["GET", "POST"])
def home():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)





