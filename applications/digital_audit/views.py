import json
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import DigitalizationAssessmentForm
from .models import DigitalizationAssessment
from django.conf import settings
import google.generativeai as genai

def llamar_ai_gemini(data):
    """Llama a Gemini para generar un informe personalizado"""
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Construir el prompt
        prompt = f"""
        ERES: Un Consultor Estratégico de Euskodev, experto en humanizar la tecnología para negocios reales.
        OBJETIVO: Generar una auditoría de digitalización que sea inspiradora y FÁCIL DE COMPRENDER, pero que mantenga un tono exclusivo y profesional. 
        
        PERFIL DE LA EMPRESA:
        - Nombre: {data.get('company_name')}
        - Sector: {data.get('business_activity')}
        
        ESTADO ACTUAL:
        - Web: {'Sí (Adaptada a móvil)' if data.get('website_responsive') == 'True' else 'Sin web moderna'}
        - Clientes: {'Usa CRM para conocer a sus clientes' if data.get('uses_crm') == 'True' else 'Gestión tradicional'}, {'Invierte en publicidad digital' if data.get('does_ads') == 'True' else 'Crecimiento orgánico'}
        - Ventas: {'Venta online activa' if data.get('sells_online') == 'True' else 'Venta presencial'}
        - Seguridad: {'Protección de datos y SSL' if data.get('has_ssl') == 'True' else 'Pendiente de blindar'}
        
        TAREA: Generar un "DOSSIER ESTRATÉGICO" comprensible:
        1. "descripcion": Una visión cercana sobre el potencial del negocio. Menos tecnicismos, más visión de futuro.
        2. "analisis_profundo": Explica por qué "esto le importa" al dueño del negocio. ¿Gana tiempo? ¿Consigue más clientes? ¿Se diferencia?
        3. "oportunidades": 4 Pasos claros y lógicos para mejorar.
        4. "recomendaciones_ai": 3 Soluciones que Euskodev puede crear (ej: "Tu oficina abierta 24h con un Agente AI", "Una web que vende sola", etc.).
        
        LENGUAJE: Cercano, elegante, motivador. Cero jerga técnica innecesaria.
dor y directo. Evita lo obvio.
        
        FORMATO DE SALIDA (SOLO JSON):
        {{
            "nivel": "Premium/Consolidado/En Crecimiento/Emergente",
            "score": 0-100,
            "descripcion": "...",
            "analisis_profundo": "...",
            "oportunidades": ["...", "..."],
            "recomendaciones_ai": ["...", "..."]
        }}
        """
        
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Limpiar posibles backticks de markdown
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text_response)
    except Exception as e:
        print(f"Error AI Gemini: {e}")
        return None

def calcular_nivel_digitalizacion(data):
    """Calcula el nivel de digitalización y mejora con IA si es posible"""
    
    # 1. Campos reales que están en el formulario actual
    preguntas = [
        'has_website', 'website_responsive', 'seo_optimized', 
        'active_social_media', 'does_ads', 'uses_crm',
        'sells_online', 'accepts_online_payments', 'uses_erp',
        'uses_whatsapp', 'has_ssl', 'gdpr_compliant'
    ]
    
    respuestas_positivas = 0
    total = len(preguntas)
    
    for pregunta in preguntas:
        valor = data.get(pregunta)
        if valor == 'True' or valor == True:
            respuestas_positivas += 1
    
    porcentaje = (respuestas_positivas / total) * 100
    
    # Intentar obtener respuesta de la IA real
    ai_result = llamar_ai_gemini(data)
    
    if ai_result:
        return {
            'nivel': ai_result.get('nivel', 'Innovador'),
            'porcentaje': round(porcentaje),
            'descripcion': ai_result.get('descripcion', 'Tu ecosistema digital muestra señales de gran potencial.'),
            'analisis_profundo': ai_result.get('analisis_profundo', 'Análisis detallado en proceso...'),
            'recomendaciones': ai_result.get('recomendaciones_ai', []),
            'oportunidades': ai_result.get('oportunidades', []),
            'ai_powered': True
        }

    # Fallback DINÁMICO (Pseudo-IA) si la conexión falla o no hay API Key
    has_web = data.get('has_website') == 'True'
    uses_crm = data.get('uses_crm') == 'True'
    sells_online = data.get('sells_online') == 'True'
    
    # Construir análisis basado en respuestas específicas
    analisis_piezas = []
    if has_web:
        if data.get('seo_optimized') == 'True':
            analisis_piezas.append("Tu web ya tiene visibilidad en buscadores, lo cual es una ventaja competitiva clave.")
        else:
            analisis_piezas.append("Aunque tienes web, la falta de optimización SEO hace que seas invisible para clientes que buscan tus servicios activamente.")
    else:
        analisis_piezas.append("La ausencia de una plataforma web propia es actualmente tu mayor freno; pierdes la oportunidad de controlar tu narrativa y tus datos.")
        
    if uses_crm:
        analisis_piezas.append("La gestión digital de tus contactos te permite escalar hacia una personalización profunda de tus servicios.")
    else:
        analisis_piezas.append("Tu gestión de clientes parece ser manual; esto genera una 'fuga de memoria' que te impide capitalizar el valor a largo plazo de tus contactos.")

    if data.get('active_social_media') == 'True':
        analisis_piezas.append("Tu presencia en redes sociales es un buen motor de comunidad, pero debe integrarse con tus sistemas de venta directa.")
    
    if data.get('has_ssl') == 'False':
        analisis_piezas.append("Hemos detectado vulnerabilidades en la confianza de tu sitio; la seguridad SSL es hoy el requisito mínimo para que un cliente se sienta seguro contigo.")

    if sells_online:
        analisis_piezas.append("La venta online ya es parte de tu ADN; ahora el objetivo es automatizarla para que no dependa de tu tiempo personal.")
    else:
        analisis_piezas.append("Limitarse al canal offline hoy en día es restringir tu crecimiento a tu ubicación física y horario comercial.")

    analisis_profundo = " ".join(analisis_piezas)
    
    if porcentaje >= 80:
        nivel = "Líder Digital"
        descripcion = f"Tu negocio para {data.get('company_name', 'tu empresa')} ya habla el lenguaje del futuro. Tienes las herramientas para dominar tu mercado."
        oportunidades = ["Crea tu propio 'cerebro' IA", "Automatiza tareas críticas", "Vende de forma hiper-personalizada", "Blindaje de datos premium"]
        recomendaciones = ["Asistente Inteligente Euskodev", "Sistema de Ventas Autónomo", "Optimización de Infraestructura"]
    elif porcentaje >= 50:
        nivel = "Potencial en Marcha"
        descripcion = "Vas por buen camino, pero todavía hay piezas que no encajan del todo para ser realmente eficiente."
        oportunidades = ["Unifica tu web y tus ventas", "Convierte visitas en clientes", "Mejora la atención con WhatsApp Pro", "Analítica de comportamiento"]
        recomendaciones = ["Rediseño de Experiencia Web", "Conexión CRM y Ventas", "Plan Estratégico de Crecimiento"]
    else:
        nivel = "Semilla Digital"
        descripcion = "Es el momento perfecto para empezar. El lienzo está en blanco y las opciones de crecimiento son infinitas."
        oportunidades = ["Lanza tu primera web profesional", "Aparece en los mapas de Google", "Digitaliza tu atención al cliente", "Protege tu identidad legal"]
        recomendaciones = ["Puesta en Marcha Digital", "Web Corporativa de Alto Impacto", "Consultoría de Inicio Tecnológico"]
    
    return {
        'nivel': nivel,
        'porcentaje': round(porcentaje),
        'descripcion': descripcion,
        'analisis_profundo': analisis_profundo,
        'recomendaciones': recomendaciones,
        'oportunidades': oportunidades,
        'ai_powered': False
    }

@csrf_exempt
def procesar_test(request):
    """Procesa el test y devuelve el resultado inmediatamente"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Calcular nivel
            resultado = calcular_nivel_digitalizacion(data)
            
            # Guardar en base de datos
            try:
                DigitalizationAssessment.objects.create(
                    company_name=data.get('company_name', ''),
                    contact_name=data.get('contact_name', ''),
                    company_email=data.get('company_email', ''),
                    contact_tel=data.get('contact_tel', ''),
                    business_activity=data.get('business_activity', ''),
                    has_website=data.get('has_website') == 'True',
                    website_responsive=data.get('website_responsive') == 'True',
                    seo_optimized=data.get('seo_optimized') == 'True',
                    active_social_media=data.get('active_social_media') == 'True',
                    does_ads=data.get('does_ads') == 'True',
                    uses_crm=data.get('uses_crm') == 'True',
                    sells_online=data.get('sells_online') == 'True',
                    accepts_online_payments=data.get('accepts_online_payments') == 'True',
                    uses_erp=data.get('uses_erp') == 'True',
                    uses_whatsapp=data.get('uses_whatsapp') == 'True',
                    has_ssl=data.get('has_ssl') == 'True',
                    gdpr_compliant=data.get('gdpr_compliant') == 'True',
                )
            except Exception as e:
                print(f"Error guardando: {e}")
            
            return JsonResponse(resultado)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


class DigitalizationAssessmentView(TemplateView):
    template_name = 'digital_audit/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DigitalizationAssessmentForm()
        context['form'] = form
        return context


class ThankYouBecaudeTheTestView(TemplateView):
    template_name= 'digital_audit/thank_you.html'
