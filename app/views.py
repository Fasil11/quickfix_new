from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from .models import *

view = Blueprint('view',__name__)


@view.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        service = request.form.get('service')
        service_pro=service_provider.query.filter(service_provider.service_type==service).all()
        return render_template('index.html',user=current_user,service_providers = service_pro)       
    return render_template('index.html',user=current_user)
@view.route('/about')
def about():
    return render_template('About.html')     
  
@view.route('/service_providers/<service>')
@login_required
def provider():
    service_pro=service_provider.query.filter(service_provider.service_type==service).all()
    return render_template('service_providers.html',user=current_user,providers = service_pro) 

# 
# def service_providers():
#     providers = service_provider.query.all() 
#     return render_template('service_providers.html', providers=providers)


@view.route('/rating/<int:request_id>', methods=['GET', 'POST'])
@login_required
def rating(request_id):
    request = ServiceRequest.query.get_or_404(request_id)

    if request.provider_id != current_user.id:
        return redirect(url_for('service_requests'))

    if request.provider_id is None:
        return redirect(url_for('service_requests'))

    if request.provider_id is not None and request.rating is not None:
        return redirect(url_for('service_requests'))

    if request.method == 'POST':
        rating = request.form['rating']
        request.rating = rating
        db.session.commit()
        return redirect(url_for('service_requests'))

    return render_template('rating.html', request=request)