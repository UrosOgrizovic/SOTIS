from rest_framework.routers import SimpleRouter

from src.exams.views import ExamViewSet, QuestionViewSet, ChoiceViewSet, DomainViewSet, SubjectViewSet, \
    ProblemAttachmentViewSet

examsRouter = SimpleRouter()
examsRouter.register(r'exams', ExamViewSet)

questionsRouter = SimpleRouter()
questionsRouter.register(r'questions', QuestionViewSet)

choicesRouter = SimpleRouter()
choicesRouter.register(r'choices', ChoiceViewSet)

domainsRouter = SimpleRouter()
domainsRouter.register(r'domains', DomainViewSet)

subjectsRouter = SimpleRouter()
subjectsRouter.register(r'subjects', SubjectViewSet)

problemAttachmentRouter = SimpleRouter()
problemAttachmentRouter.register(r'problem_attachments', ProblemAttachmentViewSet)
