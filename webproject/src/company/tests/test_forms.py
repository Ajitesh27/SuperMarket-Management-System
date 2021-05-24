import base64
from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from company.forms import EditCompanyForm

class EditCompanyFormTest(TestCase):
    def setUp(self):
        self.com_creater = EditCompanyForm()
        self.TEST_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAACcAAAAmCAYAAABH/4KQAAADC0lEQVRYR9WYvVLjMBSFj0i7PACpQkO9g+lJetieaqFJJk9B8hSZpCFU9As9To93tqZZV8kDQBtr51hWItuRLWecLNEMYwYk3U/n/uhHYIv2fSRbR0AbQEs0cAmJFn83pgohEAII5RKz330x3cIMRJVB5yN5Kxr4CRmDVWsC06qgTnAx1BHuM+pUg9O9K0CWwnkT+QCJ2+1ICkYJTIOuuCua1wrHuGoc4bUWtewEoYwwtMXkRriLkWxLBbaXJiPcbQLMwe0bbBWKETpvfeGbauTgvLGUe5ErbyRcRuj86QuWoLil4HYW/K6rzSTJCi4pFw+u8+yqX5Igg5Ry/9Gd2XWGQU+cruC+imqaUqsXu9WbyNettqRd+RaI1ROupePkGOh6gHcCNI+B+QcQLIBJACw+1pT3baD5LU89/1T92N+lLSOcivORHCT7ZuGYt64CenlXXwJenakhvZc14K8b9Tf2MxsXd32m4FwAWZiFi0upGH8uJnmDzzdpg4SjosNUOVXj9DzXT2m1N6oiMBXeWP4t2z/pKrrzx1N+Gqq3+ASCufpfEZzXBMZXSmndv8BdIeFKdwQCDNrA87ualMqYcWYaKILjIunarAcsgG5w2iWEZKyxEZJBzq8ZXzrmsvCMOY51jTnacFLOXJlOArqIKrCZBglHCKqsG/txEYOZQ6wZxpxizhYXVGNwCfCr43GTW3UiVFFNK1eYEDSczUgTNpvJtpjT8eaYDDQRspSUHsN1tg5n+SzLZrINTi+S7iVgaRPwWYR5eSk8jegSwAkZSzrYdYIM/HVSuNQ5F/dyfxXJXYGuLW16+6IKccZatq9sBpsT6+2tLDlEhI7a+B0KcSl5nR0E/KArFJzr/lqn/aK59IVndRL+SuoFPRFzmcd0p9PJrtUzr4mHccGhInu65VvF1+7UHQ7rUp1kb2lhrjP2WNOyt/1UQmSN1frsZV9J7pZvdj3MJzBzBcmLJp9X63inK3z2qqRcbZACvlziscr7cKlbbeGyUpMP1ZYHa74B81wWAb75euSaTP8AOKqR6Mi2ybIAAAAASUVORK5CYII="
        self.test_image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(self.TEST_IMAGE)),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(self.TEST_IMAGE),
            charset='utf-8',
        )
        self.com_creater2 = EditCompanyForm(
            data = {
            'logo': self.test_image,
            'name': "Super Management System",
            'address': "P.O.Box 333, Moyo",
            "company_tel": "+25473xxxxxxx"
            }
        )

    def test_company_name_field_label(self):
        self.assertFalse(self.com_creater.fields['name'].label is None)
        self.assertFalse(self.com_creater.fields['name'].label == 'name')

    def test_company_address_field_label(self):
        self.assertFalse(self.com_creater.fields['address'].label is None)
        self.assertFalse(self.com_creater.fields['address'].label == 'address')

    def test_company_tel_field_label(self):
        self.assertFalse(self.com_creater.fields['company_tel'].label is None)
        self.assertFalse(self.com_creater.fields['company_tel'].label == 'company_tel')

    def test_company_edit_form_is_not_valid(self):
        self.assertFalse(self.com_creater.is_valid())
