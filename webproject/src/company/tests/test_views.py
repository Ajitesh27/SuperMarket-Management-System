import base64
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.test import TestCase, override_settings
from django.urls import reverse_lazy
from company.models import Company

class EditCampanyViewTest(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        self.TEST_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAACcAAAAmCAYAAABH/4KQAAADC0lEQVRYR9WYvVLjMBSFj0i7PACpQkO9g+lJetieaqFJJk9B8hSZpCFU9As9To93tqZZV8kDQBtr51hWItuRLWecLNEMYwYk3U/n/uhHYIv2fSRbR0AbQEs0cAmJFn83pgohEAII5RKz330x3cIMRJVB5yN5Kxr4CRmDVWsC06qgTnAx1BHuM+pUg9O9K0CWwnkT+QCJ2+1ICkYJTIOuuCua1wrHuGoc4bUWtewEoYwwtMXkRriLkWxLBbaXJiPcbQLMwe0bbBWKETpvfeGbauTgvLGUe5ErbyRcRuj86QuWoLil4HYW/K6rzSTJCi4pFw+u8+yqX5Igg5Ry/9Gd2XWGQU+cruC+imqaUqsXu9WbyNettqRd+RaI1ROupePkGOh6gHcCNI+B+QcQLIBJACw+1pT3baD5LU89/1T92N+lLSOcivORHCT7ZuGYt64CenlXXwJenakhvZc14K8b9Tf2MxsXd32m4FwAWZiFi0upGH8uJnmDzzdpg4SjosNUOVXj9DzXT2m1N6oiMBXeWP4t2z/pKrrzx1N+Gqq3+ASCufpfEZzXBMZXSmndv8BdIeFKdwQCDNrA87ualMqYcWYaKILjIunarAcsgG5w2iWEZKyxEZJBzq8ZXzrmsvCMOY51jTnacFLOXJlOArqIKrCZBglHCKqsG/txEYOZQ6wZxpxizhYXVGNwCfCr43GTW3UiVFFNK1eYEDSczUgTNpvJtpjT8eaYDDQRspSUHsN1tg5n+SzLZrINTi+S7iVgaRPwWYR5eSk8jegSwAkZSzrYdYIM/HVSuNQ5F/dyfxXJXYGuLW16+6IKccZatq9sBpsT6+2tLDlEhI7a+B0KcSl5nR0E/KArFJzr/lqn/aK59IVndRL+SuoFPRFzmcd0p9PJrtUzr4mHccGhInu65VvF1+7UHQ7rUp1kb2lhrjP2WNOyt/1UQmSN1frsZV9J7pZvdj3MJzBzBcmLJp9X63inK3z2qqRcbZACvlziscr7cKlbbeGyUpMP1ZYHa74B81wWAb75euSaTP8AOKqR6Mi2ybIAAAAASUVORK5CYII="
        self.test_image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(self.TEST_IMAGE)),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(self.TEST_IMAGE),
            charset='utf-8',
        )
        self.company = Company.objects.get(id=1)
        self.data = {
            'logo': self.test_image,
            'name': "Super Management System",
            'address': "P.O.Box 333, Moyo",
            "company_tel": "+25473xxxxxxx"
            }
        self.username = 'admin'
        self.password = '1234@admin'

    def test_edit_campany_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_company', kwargs={'id':self.company.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'company/company.html')

    def test_edit_campany(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_company', kwargs={'id':self.company.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_campany_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_company', kwargs={'id':self.company.id}))
        self.assertEqual(response.status_code, 200)
