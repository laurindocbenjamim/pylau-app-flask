


from flask.views import View


class MTest(View):

    def __init__(self) -> None:
        super().__init__()

    def dispatch_request(self, course) :
        return f"Hello world! {course}"