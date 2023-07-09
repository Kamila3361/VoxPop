from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .repository import CommentsRepository, TopicRepository, ListCommentRepository

app = FastAPI()
templates = Jinja2Templates(directory="templates")
topic_repository = TopicRepository()
list_of_comment_repo = ListCommentRepository()

@app.get("/")
def main_page(request: Request):
    topics = topic_repository.get_all()
    return templates.TemplateResponse(
        "main_page.html", 
            {"request": request, 
             "topics": topics}
             )

@app.get("/create_topic")
def get_create_topic(request: Request):
    return templates.TemplateResponse("add_topic.html", {"request": request})

@app.post("/create_topic")
def post_create_topic(text: str=Form()):
    topic = {"text": text}
    topic_repository.save(topic)
    return RedirectResponse("/", status_code=303)


@app.get("/{topic_id}")
def get_topic_page(request: Request, topic_id: int):
    if len(topic_repository.topics) < topic_id:
        return Response(content="Not Found", media_type="text/plain", status_code=404)
    else:
        topic = topic_repository.topics[topic_id - 1]

    if topic_id
    comments = CommentsRepository()
    comments.topic_id = topic_id
    list_of_comment_repo.save(comments, topic_id)
    all_comments = comments.get_all()
    return templates.TemplateResponse(
        "topic_page.html", {
            "request": request,
            "comments": all_comments, 
            "topic": topic
        }
    )
    
@app.get("/add_comments")
def get_add_comments(request: Request):
    return templates.TemplateResponse(
        "add_comments.html", 
        {
            "request": request,
        }
    )

@app.post("/add_comments")
def post_add_comments(topic_id: int, text: str=Form(), category: str=Form()):
    comment = {"text": text, "category": category}
    comment_repo = list_of_comment_repo.get(topic_id)
    comment_repo.save(comment)
    return RedirectResponse("/{topic_id}", status_code=303)
