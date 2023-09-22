# Generated by Django 4.2.4 on 2023-09-22 17:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='auction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('initial_price', models.DecimalField(decimal_places=1, max_digits=6)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 186794))),
                ('duration_days', models.IntegerField()),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='auction_state',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=45)),
                ('book_img', models.CharField(max_length=255)),
                ('valoration', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='book_category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='book_state',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='chat_room',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.book')),
            ],
        ),
        migrations.CreateModel(
            name='forum',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 184794))),
                ('forum_img', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='forum_category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 184794))),
                ('description', models.CharField(max_length=500)),
                ('valoration', models.IntegerField()),
                ('updated_at', models.DateTimeField()),
                ('review_img', models.CharField(max_length=255)),
                ('book_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.book')),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('description', models.CharField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_days', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 181793))),
                ('direction', models.CharField(max_length=100)),
                ('user_photo', models.CharField(max_length=255)),
                ('subscript', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='user_room',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('chat_r', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.chat_room')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.CreateModel(
            name='user_role',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('role_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.role')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.CreateModel(
            name='review_like',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('review_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.review')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user'),
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 183888))),
                ('chat_r', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.chat_room')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.CreateModel(
            name='forum_user',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('forum_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.forum')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.AddField(
            model_name='forum',
            name='forum_cat_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.forum_category'),
        ),
        migrations.CreateModel(
            name='discussion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('created_by', models.CharField(max_length=45)),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 185829))),
                ('forum_us', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.forum_user')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 186794))),
                ('discussion_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.discussion')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_cat_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.book_category'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_state_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.book_state'),
        ),
        migrations.AddField(
            model_name='book',
            name='seller_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user'),
        ),
        migrations.CreateModel(
            name='auction_offer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 54, 27, 187794))),
                ('auction_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.auction')),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.user')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='auction_state_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.auction_state'),
        ),
        migrations.AddField(
            model_name='auction',
            name='book_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='LB_API.book'),
        ),
    ]
