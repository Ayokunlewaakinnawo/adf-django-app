from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from news.models import NewsPost
#from urllib.parse import urljoin

# Add the necessary imports for scraping and 
import requests
from bs4 import BeautifulSoup




# Create your views here.
def unknown(request):
    top_3_posts = NewsPost.objects.order_by('-date_added')[:3]
    context={'top_3_posts':top_3_posts}
    return render(request,'.html', context )


def newshome(request):
    try:
        # Get the most recent post
        recent_post = NewsPost.objects.latest('date_added')
        # Get all posts except the most recent one
        other_posts = NewsPost.objects.exclude(pk=recent_post.pk)[:15]
    except NewsPost.DoesNotExist:
        raise Http404("BlogPost does not exist")


    context = {
        'recent_post': recent_post,
        'other_posts': other_posts,
    }

    return render(request, 'newsmain.html', context)


def news(request, slug):
    try:
        post = NewsPost.objects.get(slug=slug)
    except NewsPost.DoesNotExist:
        raise Http404("BlogPost does not exist")

    post = NewsPost.objects.get(slug=slug)
    context={'post':post}
    return render(request, 'newsviewdetails.html', context) 



def scrape():
    #post = Post.objects.get(slug=slug)
    # Add your scraping logic here
        # ...
    scraped_dict={}
    url = "https://techcrunch.com/tag/africa/"
    res = requests.get(url)

    soup=BeautifulSoup(res.content, "html.parser")

    latest=soup.find(class_='content-wrap')
    #article = latest.find_all('div', class_='post-block')

    #number of articles
    no_of_articles=0
    articles=latest.find_all('div',class_='post-block')
    for article in articles:
        no_of_articles+=1


    #article timestamp
    #article_time_stamp=latest.find_all('time', class_="river-byline__time")

    #article title
    article_title=latest.find_all('h2', class_='post-block__title')

    #article Description
    article_desc=latest.find_all('div', class_='post-block__content')

    #article small image url
    article_image_url_small=latest.find_all('footer',class_="post-block__footer")

    #article authors
    article_authors=latest.find_all('span', class_="river-byline__authors")

    #=======================================================================


    for article in range(no_of_articles):
        #list of content for each article
        each_article=[]

        #inserting article title
        each_article.append(article_title[article].find('a').get_text().strip())
        scraped_dict[article]=each_article

        '''
        #inserting article timestamp
        raw_datetime=article_time_stamp[article]['datetime']
        raw_datetime=datetime.strptime(raw_datetime, '%Y-%m-%dT%H:%M:%S%z').astimezone()
        final_datetime=raw_datetime.strftime('%I:%M %p %Z %B %d, %Y')
        scraped_dict[article].append(final_datetime)
        #raw_datetime=parser.parse(raw_datetime).replace(tzinfo=timezone.utc).astimezone(tz=None)
        #raw_datetime=parser.parse(raw_datetime).replace(tzinfo=timezone.utc).astimezone(tz=None)
        '''


        #inserting article small image url
        scraped_dict[article].append(article_image_url_small[article].findChildren('img')[0]['src'])

        #inserting article authors
        authors_list=[]
        for author in article_authors[article].find_all('a'):
            authors_list.append(author.get_text().strip())
        scraped_dict[article].append(", ".join(authors_list))

        #article url content
        url_link= article_title[article].find('a')['href']
        scraped_dict[article].append(url_link)





        res_content = requests.get(url_link)
        soup_cont = BeautifulSoup(res_content.content, "html.parser")
        lar_image = soup_cont.find(class_='article--post')
        lat_cont = soup_cont.find('div', class_='article-content') #-->All the Article content
        cont = lat_cont.find_all('p')
        
        #insert the article full content
        all_text = lat_cont.prettify()
        scraped_dict[article].append(all_text)

        #all_text = ""
        # Loop through each <p> tag and append its text to all_text
        #for p_tag in cont:
            #all_text += p_tag.get_text()
        #scraped_dict[article].append(all_text)
        

        #article large image url
        article_image_url=lar_image.find_all('div', class_="article__featured-image-wrapper breakout")

        #inserting article Large Image
        im_url=""
        for img_element in article_image_url:
            im_url = img_element.find('img')['src']
        scraped_dict[article].append(im_url)

        #inserting article description
        each_article.append(article_desc[article].get_text().strip())
        scraped_dict[article]=each_article
    '''
    for article_post in scraped_dict.values():
        print(article_post[5])
    self.stdout.write(self.style.SUCCESS('Successfully scraped and saved to database'))
    '''

    # After scraping, check for duplicates before saving

    for article in scraped_dict.values():
        title = article[0]
        # Check if an article with this title already exists
        if not NewsPost.objects.filter(title=title).exists():
            desc = article[6]
            url = article[3]
            author = article[2]
            body = article[4]
            image1 = article[1]
            image2 = article[5]
            ''''
            base_url = 'https://www.techcrunch.com/'  # Replace with your base URL
            image1 = urljoin(base_url, article[1])
            image2 = urljoin(base_url, article[5])
            '''
            # Create and save the Post object
            post = NewsPost(title=title, desc=desc, url=url, author=author, body=body, image1=image1, image2=image2)
            post.save()
