from rest_framework import serializers
import datetime

from .models import Book, Booklog


class BookSerializer(serializers.ModelSerializer):
    remaing_book_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'book_id', 'author', 'book_genre', 'price', 'book_count', 'book_issue_date', 'book_status', 'remaing_book_count']
        read_only = ('id', 'book_id', 'book_status')

    def create(self, validated_data):
        user = self.context['request'].user

        if not user.user_type=='admin':
            raise serializers.ValidationError('Permission denied')
        user = Book.objects.create(**validated_data)
        return user  
    
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if not user.user_type=='admin':
            raise serializers.ValidationError('Permission denied')
        super().update(instance, validated_data)
        return instance
    
    def get_remaing_book_count(self, book_id):
        book_count = book_id.book_count
        book_id_no = book_id.id
        book_taken = Booklog.objects.filter(book=book_id_no)
        book = Book.objects.filter(id=book_id_no)

        if book_taken:
            no_book_taken = book_taken.filter(return_date__isnull=True).count()
            remaining_book_count = book_count - no_book_taken

            if remaining_book_count == 0:
                book_id.book_status = False
                book_id.save()
            return remaining_book_count
        return book_count
    


class BookLogSerializer(serializers.ModelSerializer):
    issue_date = serializers.CharField(
        required=False,
    )
    due_date = serializers.CharField(
        required=False,
    )
    return_date = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Booklog
        fields = ['id', 'user', 'book', 'issue_date', 'due_date', 'return_date', 'total_fine']
        read_only = ('id', 'due_date','total_fine')

    def validate(self, attrs):
        issue_date = attrs.get('issue_date')
        user = attrs.get('book')

        if issue_date:
            issue_date = datetime.datetime.strptime(issue_date, '%Y-%m-%d')
            due_date = issue_date + datetime.timedelta(days=21)
            attrs['issue_date'] = issue_date
            attrs['due_date'] = due_date.date() 
            
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = self.context['request'].user
        book_taken = validated_data['user'].id
        book_id = validated_data['book'].id
        
        if not user.user_type=='admin':
            raise serializers.ValidationError('Permission denied')
        book_log = Booklog.objects.filter(user=book_taken).count()

        if book_log > 2:
            raise serializers.ValidationError('You have already taken three books')
        book = Book.objects.filter(id=book_id).values('book_status')
      
        if book[0]['book_status']==False:
            raise serializers.ValidationError('Book is temporarily unavailable')
        return super().create(validated_data)
            
    def update(self, instance, validated_data):
        user = self.context['request'].user
        return_date = validated_data.get('return_date')

        if user.user_type=='admin':
            due_date = instance.due_date
            id = instance.id
            return_book = Booklog.objects.filter(id=id).values('return_date')

            if return_book[0]['return_date'] is None:
                days_taken = (datetime.datetime.strptime(str(return_date), '%Y-%m-%d')) - (datetime.datetime.strptime(str(due_date), '%Y-%m-%d'))
              
                if days_taken.days>= 0:
                    total_fine = (days_taken.days)*5
                    validated_data['total_fine'] = total_fine
                    return super().update(instance, validated_data)
                validated_data['total_fine'] = 0    
                return super().update(instance, validated_data)
            raise serializers.ValidationError('You have already returned this book')
        raise serializers.ValidationError('Permission denied') 
    