from django.db import models

#for each location, there will me multiple comments
#for each comment, there will be one accessibility tag
#for each comment, there will be like and dislike function

#for each location, add an ID

# Create your models here.
'''
Things to add:
geo_info:
- get user location
- user input location through pin
Check if in 20m parameter, there exists another input with the same feature, if so, refuse to add.
Connect Feature to Location
Search Bar feature to search for locations(?) if time allows
'''


class Location(models.Model):
  #single location
  #address of location
  geo_info = models.CharField(max_length=500)
  #name of location
  name = models.CharField(max_length=500)

  #a single location can have multiple accessibilities
  def __str__(self):
    return str(self.name)


class Accessibility(models.Model):
  #type of accessibility tag
  #should be able to reverse access later on
  feature = models.CharField(max_length=100)

  def __str__(self):
    return str(self.feature)


class Comment(models.Model):
  #single comment, for each location, multiple comments
  description = models.TextField()
  accessibility_rating = models.IntegerField()
  likes = models.IntegerField(default=0)
  dislikes = models.IntegerField(default=0)
  tags = models.ManyToManyField(Accessibility)
  location = models.ForeignKey(
      Location,
      on_delete = models.CASCADE,
      related_name = 'comments',
      null = True
  )
