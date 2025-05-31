from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def sql_vulnerable(request):
    username = request.GET.get('username', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{username}'")
        result = cursor.fetchone()
    return HttpResponse(f"Sonuç: {result}")


def xss_vulnerable(request):
    comment = request.GET.get('comment', '')
    return HttpResponse(f"<h3>Yorum:</h3><p>{comment}</p>")



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def csrf_vulnerable(request):
    if request.method == 'POST':
        return HttpResponse("CSRF korumasız POST alındı")
    return HttpResponse('''
        <form method="POST">
            <input type="text" name="test" value="örnek">
            <input type="submit" value="Gönder">
        </form>
    ''')


from django.contrib.auth import login, authenticate

def session_fixation_login(request):
    user = authenticate(username='admin', password='admin')
    if user:
        login(request, user)  # Session değiştirilmeden login
        return HttpResponse("Giriş başarılı, session fixation açık")
    return HttpResponse("Başarısız giriş")


from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt

# IDOR (Insecure Direct Object Reference)

def idor_vulnerable(request):
    user_id = request.GET.get('user_id')
    if not user_id or not user_id.isdigit():
        return HttpResponse("Geçerli bir kullanıcı ID'si giriniz.")

    try:
        user = User.objects.get(id=int(user_id))
        return HttpResponse(f"Kullanıcı: {user.username}, Email: {user.email}")
    except User.DoesNotExist:
        return HttpResponse("Kullanıcı bulunamadı.")



# Clickjacking (korumasız sayfa)
@xframe_options_exempt  # Güvenlik korumasını devre dışı bırak
def clickjacking_vulnerable(request):
    return HttpResponse('''
        <html>
            <head><title>Clickjacking Zafiyeti</title></head>
            <body>
                <h2>Bu sayfa iframe içinde gösterilebilir.</h2>
                <button onclick="alert('Gizli işlem yapıldı!')">Tıkla</button>
            </body>
        </html>
    ''')