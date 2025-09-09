
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
## from app import db  # No se usa
# from app.models.products import Product  # Asume que tienes un modelo Product

bp = Blueprint('store', __name__)

@bp.route('/carrito/actualizar', methods=['POST'], endpoint='actualizar_carrito')
def store_actualizar_carrito():
    cart = session.get('carrito', [])
    cantidades = request.form.get('cantidades')
    if not cantidades:
        cantidades = request.form.to_dict(flat=False).get('cantidades', {})
    if hasattr(cantidades, 'items'):
        cantidades = cantidades.items()
    for item in cart:
        str_id = str(item['id'])
        nueva_cant = request.form.get(f'cantidades[{str_id}]')
        if nueva_cant:
            try:
                item['cantidad'] = max(1, int(nueva_cant))
            except Exception:
                pass
    session['carrito'] = cart
    flash('Cantidades actualizadas', 'success')
    return redirect(url_for('store.carrito'))

@bp.route('/carrito/vaciar', endpoint='vaciar_carrito')
def store_vaciar_carrito():
    session['carrito'] = []
    flash('Carrito vaciado', 'info')
    return redirect(url_for('store.carrito'))

@bp.route('/checkout', endpoint='checkout')
def store_checkout():
    cart = session.get('carrito', [])
    if not cart:
        flash('El carrito está vacío', 'warning')
        return redirect(url_for('store.carrito'))
    # Aquí iría la lógica de pago real
    flash('¡Gracias por tu compra! (Simulación)', 'success')
    session['carrito'] = []
    return redirect(url_for('store.carrito'))

@bp.route('/')
@bp.route('/home')
def home():
    from flask_login import current_user
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Redirige a la vista del rol correspondiente
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'vendedor':
            return redirect(url_for('auth.dashboard'))
        elif current_user.role == 'proveedor':
            return redirect(url_for('auth.dashboard'))
        else:
            return redirect(url_for('auth.dashboard'))
    productos = []  # Simulación
    return render_template('home.html', productos=productos)

@bp.route('/categorias')
def categorias():
    categorias_list = [
        {
            'nombre': 'Fútbol',
            'url': '/categoria/futbol',
            'imagen': '/static/img/categorias/futbol.jpg'
        },
        {
            'nombre': 'Baloncesto',
            'url': '/categoria/baloncesto',
            'imagen': '/static/img/categorias/baloncesto.jpg'
        },
        {
            'nombre': 'Tenis',
            'url': '/categoria/tenis',
            'imagen': '/static/img/categorias/tenis.jpg'
        },
        {
            'nombre': 'Natación',
            'url': '/categoria/natacion',
            'imagen': '/static/img/categorias/natacion.jpg'
        },
        {
            'nombre': 'Ciclismo',
            'url': '/categoria/ciclismo',
            'imagen': '/static/img/categorias/ciclismo.jpg'
        },
        {
            'nombre': 'Camping',
            'url': '/categoria/camping',
            'imagen': '/static/img/categorias/camping.jpg'
        },
        {
            'nombre': 'Fitness',
            'url': '/categoria/fitness',
            'imagen': '/static/img/categorias/fitness.jpg'
        },
        {
            'nombre': 'Accesorios',
            'url': '/categoria/accesorios',
            'imagen': '/static/img/categorias/accesorios.jpg'
        }
    ]
    return render_template('categorias.html', categorias=categorias_list)

@bp.route('/categoria/<string:nombre>')
def categoria(nombre):
    productos_por_categoria = {
        'futbol': [
            {
                'id': 1,
                'nombre': 'Balón de Fútbol Profesional Nike',
                'precio': 89900,
                'imagen_url': '/static/img/productos/balon.jpg',
                'descripcion': 'Balón oficial FIFA Quality Pro 2025, tecnología aerodinámica para control preciso'
            },
            {
                'id': 2,
                'nombre': 'Guayos Nike Tiempo Elite',
                'precio': 259900,
                'imagen_url': '/static/img/productos/guayos.jpg',
                'descripcion': 'Guayos premium de cuero natural, diseño profesional para máximo control y velocidad'
            },
            {
                'id': 3,
                'nombre': 'Guantes de Portero Pro',
                'precio': 79900,
                'imagen_url': '/static/img/productos/guantes.jpg',
                'descripcion': 'Guantes profesionales con tecnología Grip Control Pro y protección anti-impacto'
            },
            {
                'id': 38,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 129900,
                'imagen_url': '/static/img/productos/set_entrenamiento.jpg',
                'descripcion': 'Kit completo de entrenamiento: conos, escaleras y marcadores profesionales'
            },
            {
                'id': 39,
                'nombre': 'Camiseta Oficial Pro',
                'precio': 189900,
                'imagen_url': '/static/img/productos/camiseta.jpg',
                'descripcion': 'Camiseta oficial con tecnología DriFit, diseño 2025 transpirable'
            }
        ],
        'baloncesto': [
            {
                'id': 4,
                'nombre': 'Balón Spalding NBA Elite',
                'precio': 219900,
                'imagen_url': 'https://images.unsplash.com/photo-1628779238951-be2c9f2a59f4?w=400&q=80',
                'descripcion': 'Balón oficial NBA 2025, tecnología de agarre avanzado y control superior'
            },
            {
                'id': 5,
                'nombre': 'Nike LeBron XX Elite',
                'precio': 589900,
                'imagen_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80',
                'descripcion': 'Zapatillas signature con Nike Air Zoom y amortiguación React de última generación'
            },
            {
                'id': 6,
                'nombre': 'Jersey NBA Elite 2025',
                'precio': 249900,
                'imagen_url': 'https://images.unsplash.com/photo-1583396796390-6da043f2ba3c?w=400&q=80',
                'descripcion': 'Jersey oficial NBA, tecnología AeroSwift 2.0 para máximo rendimiento'
            },
            {
                'id': 37,
                'nombre': 'Tablero Profesional NBA',
                'precio': 899900,
                'imagen_url': 'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=400&q=80',
                'descripcion': 'Tablero oficial regulación NBA, cristal templado premium con sistema pro-flex'
            },
            {
                'id': 40,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1574623452334-1e0ac2b3ccb4?w=400&q=80',
                'descripcion': 'Kit completo de entrenamiento: conos, balón de práctica y ejercitadores'
            }
        ],
        'tenis': [
            {
                'id': 7,
                'nombre': 'Raqueta Babolat Pure Drive',
                'precio': 799900,
                'imagen_url': 'https://images.unsplash.com/photo-1599586120429-48281b6f0ece?w=200',
                'descripcion': 'Raqueta profesional 2025, tecnología Pure Feel, marco de grafito, peso: 300g'
            },
            {
                'id': 8,
                'nombre': 'Zapatillas Nike Air Zoom Vapor',
                'precio': 459900,
                'imagen_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=200',
                'descripcion': 'Zapatillas de tenis premium con tecnología Dynamic Fit y amortiguación Zoom Air'
            },
            {
                'id': 9,
                'nombre': 'Set Wilson Tour Premier',
                'precio': 69900,
                'imagen_url': 'https://images.unsplash.com/photo-1531315396756-905d68d21b56?w=200',
                'descripcion': 'Set de 4 pelotas oficiales, aprobadas para torneos Grand Slam'
            },
            {
                'id': 31,
                'nombre': 'Raquetero Wilson Pro Staff',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1619926096619-5956ab4dfb66?w=200',
                'descripcion': 'Raquetero térmico profesional, capacidad 6 raquetas, bolsillos adicionales'
            },
            {
                'id': 32,
                'nombre': 'Pack Accesorios Pro',
                'precio': 149900,
                'imagen_url': 'https://images.unsplash.com/photo-1617083934824-446f1ada2f5e?w=200',
                'descripcion': 'Set profesional: 3 grips, 2 antivibradores, muñequeras y vincha'
            },
            {
                'id': 33,
                'nombre': 'Short Nike Court Flex',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1618354691551-44de113f0164?w=200',
                'descripcion': 'Short profesional Dri-FIT, tejido flexible y bolsillos para pelotas'
            },
            {
                'id': 34,
                'nombre': 'Polo Adidas Club',
                'precio': 119900,
                'imagen_url': 'https://images.unsplash.com/photo-1626947346165-4c2288dadc2a?w=200',
                'descripcion': 'Polo oficial con tecnología ClimaCool, tejido transpirable ultraligero'
            },
            {
                'id': 35,
                'nombre': 'Cordaje Luxilon Alu Power',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1619926096495-36085d496539?w=200',
                'descripcion': 'Cordaje premium de alta tensión (1.25mm), usado por profesionales'
            }
        ],
        'natacion': [
            {
                'id': 10,
                'nombre': 'Gafas Speedo Elite',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1600965962323-6362f726c3f5?w=400&q=80',
                'descripcion': 'Gafas profesionales con tecnología IQfit™, diseño hidrodinámico y protección UV'
            },
            {
                'id': 11,
                'nombre': 'Traje de Competición Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1575429198097-0414ec08e8cd?w=400&q=80',
                'descripcion': 'Traje FINA-approved con tecnología de compresión y tejido repelente al cloro'
            },
            {
                'id': 12,
                'nombre': 'Gorro Competición Elite',
                'precio': 39900,
                'imagen_url': 'https://images.unsplash.com/photo-1601821326018-d949a54b6402?w=400&q=80',
                'descripcion': 'Gorro de silicona premium con diseño hidrodinámico y ajuste perfecto'
            },
            {
                'id': 41,
                'nombre': 'Aletas Carbono Pro',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1530138897365-a9615cf36e7f?w=400&q=80',
                'descripcion': 'Aletas profesionales de fibra de carbono para máxima potencia'
            },
            {
                'id': 42,
                'nombre': 'Kit Elite Performance',
                'precio': 99900,
                'imagen_url': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=400&q=80',
                'descripcion': 'Kit profesional: tabla técnica, pull buoy competición y snorkel elite'
            }
        ],
        'ciclismo': [
            {
                'id': 13,
                'nombre': 'Bicicleta Specialized S-Works',
                'precio': 3499900,
                'imagen_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=400&q=80',
                'descripcion': 'Bicicleta profesional carbono, grupo Shimano Dura-Ace Di2 2025'
            },
            {
                'id': 14,
                'nombre': 'Casco Aero Elite',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1505705694340-019e1e335916?w=400&q=80',
                'descripcion': 'Casco aerodinámico con tecnología MIPS y ventilación avanzada'
            },
            {
                'id': 15,
                'nombre': 'Guantes Pro Racing',
                'precio': 69900,
                'imagen_url': 'https://images.unsplash.com/photo-1533561052604-c3beb6d55b8d?w=400&q=80',
                'descripcion': 'Guantes profesionales con gel anti-vibración y tejido premium'
            },
            {
                'id': 43,
                'nombre': 'Uniforme Elite Pro',
                'precio': 259900,
                'imagen_url': 'https://images.unsplash.com/photo-1559249634-7d50625659e9?w=400&q=80',
                'descripcion': 'Conjunto jersey y culotte con tecnología aerodinámica y tejido italiano'
            },
            {
                'id': 44,
                'nombre': 'Zapatillas Pro Carbon',
                'precio': 399900,
                'imagen_url': 'https://images.unsplash.com/photo-1572986385772-2fd6416cf7b3?w=400&q=80',
                'descripcion': 'Zapatillas de carbono profesionales con sistema BOA® y suela rígida'
            }
        ],
        'camping': [
            {
                'id': 16,
                'nombre': 'Carpa North Face Pro 4P',
                'precio': 599900,
                'imagen_url': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400&q=80',
                'descripcion': 'Carpa ultraligera 4 personas, doble capa y tecnología WeatherShield™'
            },
            {
                'id': 17,
                'nombre': 'Sleeping Bag Premium',
                'precio': 199900,
                'imagen_url': 'https://images.unsplash.com/photo-1623894404240-30256524497c?w=400&q=80',
                'descripcion': 'Saco de dormir térmico (-10°C) con tecnología ThermalPro™'
            },
            {
                'id': 18,
                'nombre': 'Linterna Pro LED',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1565049363213-4aa1cf123132?w=400&q=80',
                'descripcion': 'Linterna profesional 2000 lúmenes, resistente al agua IP67'
            },
            {
                'id': 45,
                'nombre': 'Mochila Expedition Pro',
                'precio': 329900,
                'imagen_url': 'https://images.unsplash.com/photo-1596097557993-87004ea4ddb1?w=400&q=80',
                'descripcion': 'Mochila 65L con sistema de hidratación y soporte ergonómico'
            },
            {
                'id': 46,
                'nombre': 'Kit Cocina Camping Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1510672981848-a1c4f1cb5ccf?w=400&q=80',
                'descripcion': 'Set completo de cocina outdoor: hornilla, utensilios y contenedores'
            }
        ],
        'fitness': [
            {
                'id': 19,
                'nombre': 'Set Mancuernas Pro',
                'precio': 399900,
                'imagen_url': 'https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=400&q=80',
                'descripcion': 'Set premium de mancuernas 2-30kg con rack de almacenamiento'
            },
            {
                'id': 20,
                'nombre': 'Kit Bandas Elite',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&q=80',
                'descripcion': 'Set profesional de 6 bandas con niveles progresivos de resistencia'
            },
            {
                'id': 21,
                'nombre': 'Mat Yoga Pro',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&q=80',
                'descripcion': 'Colchoneta premium antideslizante con alineación corporal'
            },
            {
                'id': 47,
                'nombre': 'Banco Ajustable Pro',
                'precio': 499900,
                'imagen_url': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=400&q=80',
                'descripcion': 'Banco multifuncional profesional con 8 posiciones'
            },
            {
                'id': 48,
                'nombre': 'Kit CrossFit Elite',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400&q=80',
                'descripcion': 'Set completo: cuerda, pelota medicinal y kettlebell'
            }
        ],
        'accesorios': [
            {
                'id': 22,
                'nombre': 'Botella Hydro Premium',
                'precio': 39900,
                'imagen_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&q=80',
                'descripcion': 'Botella térmica premium de acero inoxidable, tecnología de aislamiento 24h'
            },
            {
                'id': 23,
                'nombre': 'Bolso Training Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1596277795814-34e035da4630?w=400&q=80',
                'descripcion': 'Bolso deportivo premium con compartimentos especializados y material resistente'
            },
            {
                'id': 24,
                'nombre': 'Toalla UltraDry Elite',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1563501724843-e32930da9594?w=400&q=80',
                'descripcion': 'Toalla deportiva de microfibra premium, secado ultra rápido'
            },
            {
                'id': 25,
                'nombre': 'Smartwatch Pro GPS',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1544117519-31a4b719223d?w=400&q=80',
                'descripcion': 'Reloj inteligente con GPS integrado, monitor cardíaco y 30 modos deportivos'
            },
            {
                'id': 26,
                'nombre': 'Cinturón Pro Runner',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1461770354136-8f58567b617a?w=400&q=80',
                'descripcion': 'Cinturón deportivo ergonómico con bolsillos expandibles y material reflectivo'
            },
            {
                'id': 27,
                'nombre': 'Kit Protección Elite',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&q=80',
                'descripcion': 'Set completo de protección deportiva premium con tecnología de absorción'
            }
        ]
    }
    
    productos = productos_por_categoria.get(nombre.lower(), [])
    return render_template('categorias.html', productos=productos, categoria=nombre)

@bp.route('/producto/<int:producto_id>')
def producto(producto_id):
    # Buscar el producto real en todas las categorías
    productos_por_categoria = {
        'futbol': [
            {
                'id': 1,
                'nombre': 'Balón de Fútbol Profesional Nike',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400&q=80',
                'descripcion': 'Balón oficial FIFA Quality Pro 2025, tecnología aerodinámica para control preciso'
            },
            {
                'id': 2,
                'nombre': 'Guayos Nike Tiempo Elite',
                'precio': 259900,
                'imagen_url': 'https://images.unsplash.com/photo-1594150878496-a921e5af8907?w=400&q=80',
                'descripcion': 'Guayos premium de cuero natural, diseño profesional para máximo control y velocidad'
            },
            {
                'id': 3,
                'nombre': 'Guantes de Portero Pro',
                'precio': 79900,
                'imagen_url': 'https://images.unsplash.com/photo-1610471670560-ee84636dc9b3?w=400&q=80',
                'descripcion': 'Guantes profesionales con tecnología Grip Control Pro y protección anti-impacto'
            },
            {
                'id': 38,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=400&q=80',
                'descripcion': 'Kit completo de entrenamiento: conos, escaleras y marcadores profesionales'
            },
            {
                'id': 39,
                'nombre': 'Camiseta Oficial Pro',
                'precio': 189900,
                'imagen_url': 'https://images.unsplash.com/photo-1577212017184-33827435d3b3?w=400&q=80',
                'descripcion': 'Camiseta oficial con tecnología DriFit, diseño 2025 transpirable'
            }
        ],
        'baloncesto': [
            {
                'id': 4,
                'nombre': 'Balón Spalding NBA Elite',
                'precio': 219900,
                'imagen_url': 'https://images.unsplash.com/photo-1628779238951-be2c9f2a59f4?w=400&q=80',
                'descripcion': 'Balón oficial NBA 2025, tecnología de agarre avanzado y control superior'
            },
            {
                'id': 5,
                'nombre': 'Nike LeBron XX Elite',
                'precio': 589900,
                'imagen_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80',
                'descripcion': 'Zapatillas signature con Nike Air Zoom y amortiguación React de última generación'
            },
            {
                'id': 6,
                'nombre': 'Jersey NBA Elite 2025',
                'precio': 249900,
                'imagen_url': 'https://images.unsplash.com/photo-1583396796390-6da043f2ba3c?w=400&q=80',
                'descripcion': 'Jersey oficial NBA, tecnología AeroSwift 2.0 para máximo rendimiento'
            },
            {
                'id': 37,
                'nombre': 'Tablero Profesional NBA',
                'precio': 899900,
                'imagen_url': 'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=400&q=80',
                'descripcion': 'Tablero oficial regulación NBA, cristal templado premium con sistema pro-flex'
            },
            {
                'id': 40,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1574623452334-1e0ac2b3ccb4?w=400&q=80',
                'descripcion': 'Kit completo de entrenamiento: conos, balón de práctica y ejercitadores'
            }
        ],
        'tenis': [
            {
                'id': 7,
                'nombre': 'Raqueta Babolat Pure Drive',
                'precio': 799900,
                'imagen_url': 'https://images.unsplash.com/photo-1599586120429-48281b6f0ece?w=200',
                'descripcion': 'Raqueta profesional 2025, tecnología Pure Feel, marco de grafito, peso: 300g'
            },
            {
                'id': 8,
                'nombre': 'Zapatillas Nike Air Zoom Vapor',
                'precio': 459900,
                'imagen_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=200',
                'descripcion': 'Zapatillas de tenis premium con tecnología Dynamic Fit y amortiguación Zoom Air'
            },
            {
                'id': 9,
                'nombre': 'Set Wilson Tour Premier',
                'precio': 69900,
                'imagen_url': 'https://images.unsplash.com/photo-1531315396756-905d68d21b56?w=200',
                'descripcion': 'Set de 4 pelotas oficiales, aprobadas para torneos Grand Slam'
            },
            {
                'id': 31,
                'nombre': 'Raquetero Wilson Pro Staff',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1619926096619-5956ab4dfb66?w=200',
                'descripcion': 'Raquetero térmico profesional, capacidad 6 raquetas, bolsillos adicionales'
            },
            {
                'id': 32,
                'nombre': 'Pack Accesorios Pro',
                'precio': 149900,
                'imagen_url': 'https://images.unsplash.com/photo-1617083934824-446f1ada2f5e?w=200',
                'descripcion': 'Set profesional: 3 grips, 2 antivibradores, muñequeras y vincha'
            },
            {
                'id': 33,
                'nombre': 'Short Nike Court Flex',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1618354691551-44de113f0164?w=200',
                'descripcion': 'Short profesional Dri-FIT, tejido flexible y bolsillos para pelotas'
            },
            {
                'id': 34,
                'nombre': 'Polo Adidas Club',
                'precio': 119900,
                'imagen_url': 'https://images.unsplash.com/photo-1626947346165-4c2288dadc2a?w=200',
                'descripcion': 'Polo oficial con tecnología ClimaCool, tejido transpirable ultraligero'
            },
            {
                'id': 35,
                'nombre': 'Cordaje Luxilon Alu Power',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1619926096495-36085d496539?w=200',
                'descripcion': 'Cordaje premium de alta tensión (1.25mm), usado por profesionales'
            }
        ],
        'natacion': [
            {
                'id': 10,
                'nombre': 'Gafas Speedo Elite',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1600965962323-6362f726c3f5?w=400&q=80',
                'descripcion': 'Gafas profesionales con tecnología IQfit™, diseño hidrodinámico y protección UV'
            },
            {
                'id': 11,
                'nombre': 'Traje de Competición Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1575429198097-0414ec08e8cd?w=400&q=80',
                'descripcion': 'Traje FINA-approved con tecnología de compresión y tejido repelente al cloro'
            },
            {
                'id': 12,
                'nombre': 'Gorro Competición Elite',
                'precio': 39900,
                'imagen_url': 'https://images.unsplash.com/photo-1601821326018-d949a54b6402?w=400&q=80',
                'descripcion': 'Gorro de silicona premium con diseño hidrodinámico y ajuste perfecto'
            },
            {
                'id': 41,
                'nombre': 'Aletas Carbono Pro',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1530138897365-a9615cf36e7f?w=400&q=80',
                'descripcion': 'Aletas profesionales de fibra de carbono para máxima potencia'
            },
            {
                'id': 42,
                'nombre': 'Kit Elite Performance',
                'precio': 99900,
                'imagen_url': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=400&q=80',
                'descripcion': 'Kit profesional: tabla técnica, pull buoy competición y snorkel elite'
            }
        ],
        'ciclismo': [
            {
                'id': 13,
                'nombre': 'Bicicleta Specialized S-Works',
                'precio': 3499900,
                'imagen_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=400&q=80',
                'descripcion': 'Bicicleta profesional carbono, grupo Shimano Dura-Ace Di2 2025'
            },
            {
                'id': 14,
                'nombre': 'Casco Aero Elite',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1505705694340-019e1e335916?w=400&q=80',
                'descripcion': 'Casco aerodinámico con tecnología MIPS y ventilación avanzada'
            },
            {
                'id': 15,
                'nombre': 'Guantes Pro Racing',
                'precio': 69900,
                'imagen_url': 'https://images.unsplash.com/photo-1533561052604-c3beb6d55b8d?w=400&q=80',
                'descripcion': 'Guantes profesionales con gel anti-vibración y tejido premium'
            },
            {
                'id': 43,
                'nombre': 'Uniforme Elite Pro',
                'precio': 259900,
                'imagen_url': 'https://images.unsplash.com/photo-1559249634-7d50625659e9?w=400&q=80',
                'descripcion': 'Conjunto jersey y culotte con tecnología aerodinámica y tejido italiano'
            },
            {
                'id': 44,
                'nombre': 'Zapatillas Pro Carbon',
                'precio': 399900,
                'imagen_url': 'https://images.unsplash.com/photo-1572986385772-2fd6416cf7b3?w=400&q=80',
                'descripcion': 'Zapatillas de carbono profesionales con sistema BOA® y suela rígida'
            }
        ],
        'camping': [
            {
                'id': 16,
                'nombre': 'Carpa North Face Pro 4P',
                'precio': 599900,
                'imagen_url': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400&q=80',
                'descripcion': 'Carpa ultraligera 4 personas, doble capa y tecnología WeatherShield™'
            },
            {
                'id': 17,
                'nombre': 'Sleeping Bag Premium',
                'precio': 199900,
                'imagen_url': 'https://images.unsplash.com/photo-1623894404240-30256524497c?w=400&q=80',
                'descripcion': 'Saco de dormir térmico (-10°C) con tecnología ThermalPro™'
            },
            {
                'id': 18,
                'nombre': 'Linterna Pro LED',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1565049363213-4aa1cf123132?w=400&q=80',
                'descripcion': 'Linterna profesional 2000 lúmenes, resistente al agua IP67'
            },
            {
                'id': 45,
                'nombre': 'Mochila Expedition Pro',
                'precio': 329900,
                'imagen_url': 'https://images.unsplash.com/photo-1596097557993-87004ea4ddb1?w=400&q=80',
                'descripcion': 'Mochila 65L con sistema de hidratación y soporte ergonómico'
            },
            {
                'id': 46,
                'nombre': 'Kit Cocina Camping Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1510672981848-a1c4f1cb5ccf?w=400&q=80',
                'descripcion': 'Set completo de cocina outdoor: hornilla, utensilios y contenedores'
            }
        ],
        'fitness': [
            {
                'id': 19,
                'nombre': 'Set Mancuernas Pro',
                'precio': 399900,
                'imagen_url': 'https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=400&q=80',
                'descripcion': 'Set premium de mancuernas 2-30kg con rack de almacenamiento'
            },
            {
                'id': 20,
                'nombre': 'Kit Bandas Elite',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&q=80',
                'descripcion': 'Set profesional de 6 bandas con niveles progresivos de resistencia'
            },
            {
                'id': 21,
                'nombre': 'Mat Yoga Pro',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&q=80',
                'descripcion': 'Colchoneta premium antideslizante con alineación corporal'
            },
            {
                'id': 47,
                'nombre': 'Banco Ajustable Pro',
                'precio': 499900,
                'imagen_url': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=400&q=80',
                'descripcion': 'Banco multifuncional profesional con 8 posiciones'
            },
            {
                'id': 48,
                'nombre': 'Kit CrossFit Elite',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400&q=80',
                'descripcion': 'Set completo: cuerda, pelota medicinal y kettlebell'
            }
        ],
        'accesorios': [
            {
                'id': 22,
                'nombre': 'Botella Hydro Premium',
                'precio': 39900,
                'imagen_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&q=80',
                'descripcion': 'Botella térmica premium de acero inoxidable, tecnología de aislamiento 24h'
            },
            {
                'id': 23,
                'nombre': 'Bolso Training Pro',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1596277795814-34e035da4630?w=400&q=80',
                'descripcion': 'Bolso deportivo premium con compartimentos especializados y material resistente'
            },
            {
                'id': 24,
                'nombre': 'Toalla UltraDry Elite',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1563501724843-e32930da9594?w=400&q=80',
                'descripcion': 'Toalla deportiva de microfibra premium, secado ultra rápido'
            },
            {
                'id': 25,
                'nombre': 'Smartwatch Pro GPS',
                'precio': 299900,
                'imagen_url': 'https://images.unsplash.com/photo-1544117519-31a4b719223d?w=400&q=80',
                'descripcion': 'Reloj inteligente con GPS integrado, monitor cardíaco y 30 modos deportivos'
            },
            {
                'id': 26,
                'nombre': 'Cinturón Pro Runner',
                'precio': 49900,
                'imagen_url': 'https://images.unsplash.com/photo-1461770354136-8f58567b617a?w=400&q=80',
                'descripcion': 'Cinturón deportivo ergonómico con bolsillos expandibles y material reflectivo'
            },
            {
                'id': 27,
                'nombre': 'Kit Protección Elite',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&q=80',
                'descripcion': 'Set completo de protección deportiva premium con tecnología de absorción'
            }
        ]
    }
    all_products = []
    for lista in productos_por_categoria.values():
        all_products.extend(lista)
    prod = next((p for p in all_products if p['id'] == producto_id), None)
    if not prod:
        prod = {'id': producto_id, 'nombre': 'Producto no encontrado', 'descripcion': '', 'precio': 0, 'imagen_url': ''}
        relacionados = []
    else:
        # Relacionados: otros productos de la misma categoría
        categoria_rel = next((cat for cat, lista in productos_por_categoria.items() if any(p['id'] == producto_id for p in lista)), None)
        relacionados = [p for p in productos_por_categoria.get(categoria_rel, []) if p['id'] != producto_id][:4]
    return render_template('producto.html', producto=prod, relacionados=relacionados)

@bp.route('/carrito')
def carrito():
    cart = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in cart) if cart else 0
    return render_template('carrito.html', carrito=cart, total=total)

@bp.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    # Buscar el producto real en todas las categorías
    # Usar la misma estructura de productos que en la función producto()
    productos_por_categoria = {
        'futbol': [
            {
                'id': 1,
                'nombre': 'Balón de Fútbol Profesional Nike',
                'precio': 89900,
                'imagen_url': 'https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400&q=80',
                'descripcion': 'Balón oficial FIFA Quality Pro 2025, tecnología aerodinámica para control preciso'
            },
            {
                'id': 2,
                'nombre': 'Guayos Nike Tiempo Elite',
                'precio': 259900,
                'imagen_url': 'https://images.unsplash.com/photo-1594150878496-a921e5af8907?w=400&q=80',
                'descripcion': 'Guayos premium de cuero natural, diseño profesional para máximo control y velocidad'
            },
            {
                'id': 3,
                'nombre': 'Guantes de Portero Pro',
                'precio': 79900,
                'imagen_url': 'https://images.unsplash.com/photo-1610471670560-ee84636dc9b3?w=400&q=80',
                'descripcion': 'Guantes profesionales con tecnología Grip Control Pro y protección anti-impacto'
            },
            {
                'id': 38,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 129900,
                'imagen_url': 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=400&q=80',
                'descripcion': 'Kit completo de entrenamiento: conos, escaleras y marcadores profesionales'
            },
            {
                'id': 39,
                'nombre': 'Camiseta Oficial Pro',
                'precio': 189900,
                'imagen_url': 'https://images.unsplash.com/photo-1577212017184-33827435d3b3?w=400&q=80',
                'descripcion': 'Camiseta oficial con tecnología DriFit, diseño 2025 transpirable'
            }
        ],
        'baloncesto': [
            {
                'id': 4,
                'nombre': 'Balón Spalding NBA Elite',
                'precio': 219900,
                'imagen_url': 'https://images.unsplash.com/photo-1628779238951-be2c9f2a59f4?w=400&q=80',
                'descripcion': 'Balón oficial NBA 2025, tecnología de agarre avanzado y control superior'
            },
            {
                'id': 5,
                'nombre': 'Nike LeBron XX Elite',
                'precio': 589900,
                'imagen_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80',
                'descripcion': 'Zapatillas signature con Nike Air Zoom y amortiguación React de última generación'
            },
            {
                'id': 6,
                'nombre': 'Jersey NBA Elite 2025',
                'precio': 249900,
                'imagen_url': 'https://images.unsplash.com/photo-1583396796390-6da043f2ba3c?w=400&q=80',
                'descripcion': 'Jersey oficial NBA, tecnología AeroSwift 2.0 para máximo rendimiento'
            },
            {
                'id': 37,
                'nombre': 'Tablero Profesional NBA',
                'precio': 899900,
                'imagen_url': 'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=400&q=80',
                'descripcion': 'Tablero oficial regulación NBA, cristal templado premium con sistema pro-flex'
            },
            {
                'id': 40,
                'nombre': 'Set Entrenamiento Elite',
                'precio': 159900,
                'imagen_url': 'https://images.unsplash.com/photo-1574623452334-1e0ac2b3ccb4?w=400&q=80',
                'descripcion': 'Kit completo de entrenamiento: conos, balón de práctica y ejercitadores'
            }
        ],
        # ...agrega aquí el resto de categorías copiando la estructura de la función producto...
        'tenis': [],
        'natacion': [],
        'ciclismo': [],
        'camping': [],
        'fitness': [],
        'accesorios': []
    }
    # Unir todos los productos en una sola lista
    all_products = []
    for lista in productos_por_categoria.values():
        all_products.extend(lista)
    prod = next((p for p in all_products if p['id'] == producto_id), None)
    if not prod:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('store.carrito'))
    cantidad = int(request.form.get('cantidad', 1))
    item = {
        'id': prod['id'],
        'nombre': prod['nombre'],
        'precio': prod['precio'],
        'cantidad': cantidad,
        'imagen_url': prod.get('imagen_url', '')
    }
    cart = session.get('carrito', [])
    # Si el producto ya está en el carrito, suma la cantidad
    for p in cart:
        if p['id'] == item['id']:
            p['cantidad'] += cantidad
            break
    else:
        cart.append(item)
    session['carrito'] = cart
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('store.carrito'))

@bp.route('/carrito/eliminar/<int:producto_id>')
def eliminar_carrito(producto_id):
    cart = session.get('carrito', [])
    cart = [item for item in cart if item['id'] != producto_id]
    session['carrito'] = cart
    flash('Producto eliminado del carrito', 'info')
    return redirect(url_for('store.carrito'))
