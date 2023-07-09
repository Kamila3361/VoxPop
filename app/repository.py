class CommentsRepository:
    def __init__(self) -> None:
        self.comments = [] #{"id":, "text":, "category":}

    def get_all(self):
        return self.comments
    
    def get_next_id(self):
        return len(self.comments) + 1
    
    def save(self, comment):
        if "id" not in comment or not comment["id"]:
            comment["id"] = self.get_next_id()
        self.comments.insert(0, comment)
        return comment
    
class ListCommentRepository:
    def __init__(self) -> None:
        self.list_of_comments = {} #{"id": }
    
    def save(self, comment_repo, topic_id):
        self.list_of_comments[topic_id] = comment_repo

    def get(self, topic_id):
        if topic_id in self.list_of_comments:
            return self.list_of_comments[topic_id]
        return False

class TopicRepository:
    def __init__(self) -> None:
        self.topics = [] #{"id":, "text":, "time":}

    def get(self, start_index, end_index):
        return self.topics[start_index:end_index]

    def get_next_id(self):
        return len(self.topics) + 1
    
    def save(self, topic):
        if "id" not in topic or not topic["id"]:
            topic["id"] = self.get_next_id()
        self.topics.append(topic)
        return topic
