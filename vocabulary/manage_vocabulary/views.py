from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import authentication, serializers
from rest_framework.response import Response
from core.models import Word
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import JsonResponse
from django.db.models import Q
from manage_vocabulary.serializers import WordSerializer
import logging


logger = logging.getLogger(__name__)

# Create your views here.
class VocabularyListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(template_name='manage_vocabulary/vocabulary_list.html')


class WordList(APIView):
    permission_classes = []
    def get(self, request):
        user = self.request.user
        # From datatable pipeline function
        draw = int(request.GET.get('draw', 0))
        order_col_i = int(request.GET.get('order[0][column]', 0))
        order_dir = request.GET.get('order[0][dir]', None)
        start_i = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 0))
        search_key = request.GET.get('search[value]', '')

        recordsTotal = Word.objects.all().count()
        words, recordsFiltered = self.get_filtered_words(start_i, length, order_col_i, order_dir, search_key, user.id)
        
        data = []
        for word in words:
            data.append({'id': word.id, 'word': word.string, 'description': word.description, 'usage': word.usage, 'creator': word.creator})

        return JsonResponse({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': data})


    def get_filtered_words(self, start_i, length, order_col_i, order_dir, search_key, user_id):
        """
        Parameters:
            start_i: int
                Row start index
            length: int
                Number of rows to fetch
            order_col_i: int
                Column index by which ordering will be done
            order_dir: str
                Order direction (asc or desc)
            search_key: str
                Search keyword
        """

        columns = ['id', 'string', 'description', 'usage', 'creator']
        order_col = columns[order_col_i]
        if order_dir == 'desc':
            order_col = '-' + order_col

        if search_key:
            words = Word.objects.all(
                                    (Q(id__icontains=search_key) |
                                    Q(word__icontains=search_key) |
                                    Q(description__icontains=search_key) |
                                    Q(usage__icontains=search_key) |
                                    Q(creator__icontains=search_key))).order_by(order_col)
            filter_length = words.count()
        else:
            words = Word.objects.all().order_by(order_col)
            
            filter_length = words.count()

        words = words[start_i:start_i+length]
        
        return words, filter_length

    def post(self, request):
        user = self.request.user
        word = request.POST.get('word')
        description = request.POST.get('description')
        usage = request.POST.get('usage')
        creator = request.POST.get('creator')
        
        word = word.strip()
        if not Word.objects.filter(string=word).exists():
            new_word = Word.objects.create(
                string=word.strip(),
                description=description,
                usage=usage,
                creator=creator
            )

            new_word = Word.objects.filter(id=new_word.id)
            serializer = WordSerializer(new_word)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    # def delete(self, request):
    #     user = self.request.user
    #     print(request)
    #     word_id = request.POST.get('word_id', None)
    #     return Response(status=HTTP_200_OK)
    #     if word_id:
    #         if Word.objects.filter(id=word_id).exists():
    #             word = Word.objects.filter(id=word_id)
    #             word.delete()

    #             data = {
    #                 'deleted': True
    #             }
    #             return Response(data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user = self.request.user
        word_id = request.POST.get('word_id', None)
        string = request.POST.get('string', None)
        description = request.POST.get('description', None)
        usage = request.POST.get('usage', None)
        creator = request.POST.get('creator', None)

        if word_id:
            if Word.objects.filter(id=word_id).exists():
                word = Word.objects.get(id=word_id)

                word.string = string
                word.description = description
                word.usage = usage
                word.creator = creator

                word.save()

                word = Word.objects.filter(id=word_id)
                serializer = WordSerializer(word, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class WordInformation(APIView):
    permission_classes = []

    def get(self, request):
        word_id = request.GET.get('id', None)

        user = self.request.user

        if word_id:
            if Word.objects.filter(id=word_id).exists():
                word = Word.objects.filter(id=word_id)
                serializer = WordSerializer(word, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WordDelete(DestroyAPIView):
    permission_classes = []
    authentication_classes = []

    def delete(self, request):
        user = self.request.user
        word_id = request.POST.get('word_id', None)
        if word_id:
            if Word.objects.filter(id=word_id).exists():
                word = Word.objects.filter(id=word_id)
                word.delete()

                data = {
                    'deleted': True
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)