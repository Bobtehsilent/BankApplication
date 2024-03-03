from flask import session

def update_breadcrumb(name, url):
    if 'breadcrumb' not in session:
        session['breadcrumb'] = []

    new_crumb = {'name': name, 'url': url}
    if session['breadcrumb']:
        if url in [crumb['url'] for crumb in session['breadcrumb']]:
            session['breadcrumb'] = session['breadcrumb'][:[crumb['url'] for crumb in session['breadcrumb']].index(url)+1]
        else:
            session['breadcrumb'].append(new_crumb)
    else:
        session['breadcrumb'].append(new_crumb)

    session['breadcrumb'] = session['breadcrumb'][-5:]

    session.modified = True

def pop_breadcrumb():
    if 'breadcrumb' in session and session['breadcrumb']:
        session['breadcrumb'].pop()
        session.modified = True

def clear_breadcrumb():
    session.pop('breadcrumb', None)