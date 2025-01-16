from src.genservice.models import FeedbackGen
from src.basedao.basedao import BaseDAO


class FeedbacksDAO(BaseDAO):
    model = FeedbackGen
