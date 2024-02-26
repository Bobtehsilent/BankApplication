from flask import session

def update_breadcrumb(name, url):
    # Initialize breadcrumb if not present
    if 'breadcrumb' not in session:
        session['breadcrumb'] = []

    new_crumb = {'name': name, 'url': url}
    if session['breadcrumb']:
        # Check if the new URL is a step back in the breadcrumb
        if url in [crumb['url'] for crumb in session['breadcrumb']]:
            # Trim breadcrumb to the current URL
            session['breadcrumb'] = session['breadcrumb'][:[crumb['url'] for crumb in session['breadcrumb']].index(url)+1]
        else:
            # Append the new breadcrumb
            session['breadcrumb'].append(new_crumb)
    else:
        # If breadcrumb is empty, just add the new crumb
        session['breadcrumb'].append(new_crumb)

    # Limit the breadcrumb size to avoid excessive length
    session['breadcrumb'] = session['breadcrumb'][-5:]

    session.modified = True

def pop_breadcrumb():
    if 'breadcrumb' in session and session['breadcrumb']:
        session['breadcrumb'].pop()
        session.modified = True

def clear_breadcrumb():
    session.pop('breadcrumb', None)