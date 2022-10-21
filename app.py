#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, session

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import collections
collections.Callable = collections.abc.Callable
from sqlalchemy import func

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
from models import db, Artist, Venue, Show
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:mmm@localhost:5431/fyyr'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



   
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
print(datetime.now().year)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]

  
  all_areas = Venue.query.all()
  print(all_areas)
  
  data = []
  nb=0
  res=[]
 
  
  for i in all_areas:
  	
    data.append({'city':i.city,'state':i.state})
  for i in data:
  	nb=0
  	for j in data:
  		if(i==j):
  			nb=nb+1
  	if(nb>1):	
         	data.remove(i)
  
  ##############################################
  data1=[]
  for area in range(len(data)):
  	
    
   
    
    area_venues = Venue.query.filter_by(state=data[area]['state']).filter_by(city=data[area]['city']).all()
 	   
    
    venue_data = []
    
    
    print(area_venues)
    for venue in area_venues:
      venue_data.append({
        "id": venue.id,
        "name": venue.name,
}
        )
    data1.append({
      "city": data[area]['city'],
      "state": data[area]['state'], 
      "venues": venue_data
    })

  return render_template('pages/venues.html', areas=data1);
  
@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  description = request.form.get('search_term', '')
  x=Venue.query.filter(Venue.name.ilike(f'%{description}%')).all()
  responslist=[]
  
  
  upcoming_shows=[]
  
  print(x)
  count=len(x)	 
  
  for i in x:
   upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id==i.id).filter(Show. start_time>datetime.now()).all()
   responslist.append({"id":i.id, "name": i.name,"num_upcoming_shows":len(upcoming_shows)})
  response={
    "count": count,
    "data": responslist
  }  	
  
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  result=Show.query.all()
  l1=[]
  for a in result:
  	if(a.venue_id==venue_id):
  		l1.append(a)
    		
 
  upcoming_shows=[]

  
  
	  	
  	 
  next_shows=db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime.now()).all() 
  for i in next_shows:
    p=Artist.query.get(int(i.artist_id))
    upcoming_shows.append({"artist_id":p.id,"artist_name":p.name,"artist_image_link":p.image_link,"start_time":i.start_time})
  past_shows=[]
  
  
  	
   
  	 
  old_shows=db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all() 	
  for i in old_shows: 
	  
	       p=Artist.query.get(int(i.artist_id))
	       past_shows.append({"artist_id":p.id,"artist_name":p.name,"artist_image_link":p.image_link,"start_time":i.start_time})		
	  
  singer=Venue.query.get(venue_id)
  data={
    "id": venue_id,
    "name": singer.name,
    "genres": "homme",
    "city": singer.city,
    "state": singer.state,
    "phone": singer.phone,
     "address":singer.address,
    "website": singer.website_link,
    "facebook_link":  singer.facebook_link,
    "seeking_venue": True,
    "seeking_description": singer.desc,
    "image_link":  singer.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count":len(upcoming_shows) ,
     	}
  
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
 
  try:
	  form = VenueForm(request.form)
	  venue = Venue(
	  genre = form.genres.data,
	  name = form.name.data,
	  city = form.city.data,
	  state = form.state.data,
	  address = form.address.data,
	  phone = form.phone.data,
	  image_link = form.image_link.data,
	  facebook_link = form.facebook_link.data,
	  website_link =form.website_link.data,
	  desc = form.seeking_description.data,
	  talent=True)	  
	  db.session.add(venue)
	  db.session.commit()
  except:
    error = True
    db.session.rollback()
    
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
     flash('Venue ' + request.form['name'] + ' was successfully listed!') 	
   

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
   print(venue_id)
   Venue.query.filter_by(id=venue_id).delete()
   db.session.commit()
   	
  
  
   return render_template('pages/home.html')
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  data=[]
  base=Artist.query.all()
  
  for i in base:
     data.append(
     {
	"id":i.id,
	"name":i.name     
     
     }
     )
  	
  	
  data1=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
 
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  
  
  description = request.form.get('search_term', '')
  x=Artist.query.filter(Artist.name.ilike(f'%{description}%')).all()
  count=len(x)
  responslist=[]
  
  
  upcoming_shows=[]
  nb=0
  
  for i in x:
  
   if Show.query.filter_by(artist_id=i.id):
    	
	   upcoming_shows = db.session.query(Show).join(Artist).filter(Show.artist_id==i.id).filter(Show.start_time>datetime.now()).all()
	   responslist.append({"id":i.id, "name": i.name,"num_upcoming_shows":len(upcoming_shows)})
  response={
    "count": count,
    "data": responslist
  }  
  print(responslist)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
 
  
  
  upcoming_shows=[]
  	 
  next_shows=db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime.now()).all() 
  for i in next_shows:
    p=Venue.query.get(int(i.venue_id))
    upcoming_shows.append({"venue_id":p.id,"venue_name":p.name,"venue_image_link":p.image_link,"start_time":i.start_time})
  past_shows=[]
  
  
  	
   
   
  old_shows=db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all() 	
  for i in old_shows: 
	       p=Venue.query.get(int(i.venue_id))
	       past_shows.append({"venue_id":p.id,"venue_name":p.name,"venue_image_link":p.image_link,"start_time":i.start_time})
	      
	       	
  singer=Artist.query.get(artist_id)	
  	
  data={
    "id": artist_id,
    "name": singer.name,
    "genres": "homme",
    "city": singer.city,
    "state": singer.state,
    "phone": singer.phone,
    "website": singer.website_link,
    "facebook_link":  singer.facebook_link,
    "seeking_venue": True,
    "seeking_description": singer.desc,
    "image_link":  singer.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count":len(upcoming_shows) ,
     	}


  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  artist=Artist.query.get(artist_id)
  
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website_link
  form.seeking_talent=artist.talent
  form.seeking_description.data = artist.desc
  
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  form=FormEdit(request.form)
  x=Artist.query.get(artist_id)
  x.id=artist_id
  x.genres = form.genres.data
  

  x.name = form.name.data,
  x.city = form.city.data,
  x.state =form.state.data,
  
  x.phone =form.phone.data,
  x.image_link = form.image_link.data,
  x.facebook_link = form.facebook_link.data,
  x.website_link = form.website_link.data,
  x.desc = form.seeking_description.data,
  x.talent = True if 'seeking_talent' in request.form else False 
  db.session.commit()
    




 	
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  
  artist=Venue.query.get(venue_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genre
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website_link
  form.address.data = artist.address
  form.seeking_description.data = artist.desc
  db.session.commit()
  return render_template('forms/edit_venue.html', form=form, venue=artist)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  form=FormEdit(request.form)
  x=Venue.query.get(venue_id)
  x.id=venue_id
  x.genre = form.genres.data
  x.name = form.name.data
  x.city = form.city.data
  x.state = form.state.data
  x.address =form.address.data
  x.phone = form.phone.data
  x.image_link =form.image_link.data
  x.facebook_link =form.facebook_link.data
  x.website_link = form.website_link.data
  x.desc = form.seeking_description.data
  x.talent = True if 'seeking_talent' in request.form else False 
  db.session.commit()
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
 
  error = False
  
  try:
   
     a=Artist.query.all()
     max=a[0].id
    
     for i in a :
       if(i.id>max):
        max=i.id
    		
     form = ArtistForm(request.form)
     artist = Artist(
     id=max+1,
     genres = form.genres.data,
     name = form.name.data,
     city = form.city.data,
     state = form.state.data,
     phone = form.phone.data,
     image_link = form.image_link.data,
     facebook_link = form.facebook_link.data,
     website_link =form.website_link.data, 
     desc = form.seeking_description.data,
     talent=True)	  
     db.session.add(artist)
     db.session.commit()
  except:
    error = True
    db.session.rollback()
 
  finally:
    db.session.close()
  if error:
    
      flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
  else:
   flash('Artist ' + request.form['name'] + ' was successfully listed!')
     
    	 	
  return render_template('pages/home.html')
  
 

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  shows=Show.query.all()
  for show in shows:
  	data.append(
  	{ "venue_id": show.venue_id,
    	"venue_name": Venue.query.get(show.venue_id).name,
    	"artist_id": show.artist_id,
    	"artist_image_link":Artist.query.get(show.artist_id).image_link,
    	 "start_time":show.start_time
  	
  	}
  	)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  compteur=0
  try:
    form=ShowForm(request.form)	
    x=Show.query.all()
    compteur=len(x)
    p=Show(id=1+compteur,  
    artist_id = form.artist_id.data,
    venue_id = form.venue_id.data,
    start_time =form.start_time.data)
    
    db.session.add(p)
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
    
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
