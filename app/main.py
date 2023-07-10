from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .repository import CommentsRepository, TopicRepository, ListCommentRepository

app = FastAPI()
templates = Jinja2Templates(directory="templates")
topic_repository = TopicRepository()
list_of_comment_repo = ListCommentRepository()

@app.get("/")
def main_page(request: Request, page: int=1, limit: int=10):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    topics = topic_repository.get(start_index, end_index)
    return templates.TemplateResponse(
        "main_page.html", 
            {"request": request, 
             "topics": topics}
             )

@app.get("/create_topic")
def get_create_topic(request: Request):
    return templates.TemplateResponse("add_topic.html", {"request": request})

@app.post("/")
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

    if list_of_comment_repo.get(topic_id) == False:
        comments = CommentsRepository()
        list_of_comment_repo.save(comments, topic_id)
    else:
        comments = list_of_comment_repo.get(topic_id)
    all_comments = comments.get_all()
    return templates.TemplateResponse(
        "topic_page.html", {
            "request": request,
            "comments": all_comments, 
            "topic": topic
        }
    )
    
@app.get("/{topic_id}/add_comments/new")
def get_add_comments(request: Request, topic_id: int):
    topic = topic_repository.topics[topic_id - 1]
    return templates.TemplateResponse(
        "add_comments.html", 
        {
            "request": request,
            "topic": topic
        }
    )

@app.post("/{topic_id}")
def post_add_comments(topic_id: int, text: str=Form(), category: str=Form()):
    comment = {"text": text, "category": category}
    comment_repo = list_of_comment_repo.get(topic_id)
    comment_repo.save(comment)
    return RedirectResponse(f"/{topic_id}", status_code=303)
