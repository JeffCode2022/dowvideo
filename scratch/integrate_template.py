# scratch/integrate_template.py
import os
import re

def integrate():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(workspace_dir, "template_web_3d.txt")
    output_path = os.path.join(workspace_dir, "templates", "index.html")

    print(f"Leyendo plantilla original desde: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reemplazo de Título y Metadatos SEO
    html = html.replace(
        "<title>Agnos - Creative Agency Framer Template</title>",
        "<title>⚡ FlowGet - Descarga y Convierte Video y Audio al Instante</title>"
    )
    
    html = html.replace(
        '<meta name="description" content="Showcase your studio with a premium agency template featuring clean layouts, strong visuals, and CMS-powered sections designed to convert clients effectively.">',
        '<meta name="description" content="FlowGet es el descargador de video y audio más rápido y premium del mercado. Descarga y convierte videos de YouTube, TikTok, Instagram y más en Full HD y MP3 320kbps de forma limpia, directa y sin publicidad.">'
    )

    # 2. Reemplazo Quirúrgico del Logo
    # Buscamos la etiqueta de la imagen del logotipo original y la sustituimos por el logotipo de texto luminoso de FlowGet
    logo_target = '<img decoding="async" width="107" height="34" src="https://framerusercontent.com/images/GDUrAGnKW4Je8J3NK9BnBqUiV0k.svg?width=107&amp;height=34" alt="Brand Logo" style="display:block;width:100%;height:100%;border-radius:inherit;corner-shape:inherit;object-position:center;object-fit:contain">'
    logo_replacement = '<div style="font-family:\'Geist\',sans-serif;font-size:1.6rem;font-weight:900;color:#fff;letter-spacing:-0.03em;display:flex;align-items:center;gap:6px;position:relative;z-index:10;user-select:none;">Flow<span style="color:#ff6321;">Get</span></div>'
    html = html.replace(logo_target, logo_replacement)

    # 3. Modificación del Título y Subtítulo del Hero
    hero_title_target = 'We design brands that move <span style="--framer-text-color:var(--token-0ac79161-3e62-4c56-9251-a6a7b0ea22d3, rgb(255, 99, 33))" class="framer-text">people</span>'
    hero_title_replacement = 'Descarga videos y audios al <span style="--framer-text-color:var(--token-0ac79161-3e62-4c56-9251-a6a7b0ea22d3, rgb(255, 99, 33))" class="framer-text">instante</span>'
    html = html.replace(hero_title_target, hero_title_replacement)

    hero_desc_target = 'We combine strategy, design, and technology to help ambitious brands stand out &amp; create meaningful digital experiences.'
    hero_desc_replacement = 'FlowGet combina velocidad extrema y un diseño cristalino para que descargues y conviertas tus contenidos favoritos en Full HD y MP3 de alta fidelidad, directamente a tu almacenamiento.'
    html = html.replace(hero_desc_target, hero_desc_replacement)

    # 4. Inyección del Downloader Card en el bloque de Botones
    # Localizamos el bloque de botones '<div class="framer-1xk51t1" data-framer-name="Buttons">' y lo reemplazamos
    downloader_html = """<div class="framer-1xk51t1" data-framer-name="Buttons" style="display:block; width:100%; max-width:680px; margin:40px auto 0; position:relative; overflow:visible;">
        <div class="flowget-downloader-wrapper">
            <div class="downloader-spotlight" id="dl-spotlight"></div>
            <div class="downloader-card-glass">
                <!-- Plataformas sugeridas -->
                <div class="platform-grid-agnos">
                    <div class="platform-item-agnos" data-platform="youtube" onclick="suggestPlatform('YouTube')">
                        <i data-lucide="youtube"></i>
                        <span>YouTube</span>
                    </div>
                    <div class="platform-item-agnos" data-platform="tiktok" onclick="suggestPlatform('TikTok')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"></path></svg>
                        <span>TikTok</span>
                    </div>
                    <div class="platform-item-agnos" data-platform="instagram" onclick="suggestPlatform('Instagram')">
                        <i data-lucide="instagram"></i>
                        <span>Instagram</span>
                    </div>
                    <div class="platform-item-agnos" data-platform="twitter" onclick="suggestPlatform('Twitter')">
                        <i data-lucide="twitter"></i>
                        <span>Twitter / X</span>
                    </div>
                    <div class="platform-item-agnos" data-platform="facebook" onclick="suggestPlatform('Facebook')">
                        <i data-lucide="facebook"></i>
                        <span>Facebook</span>
                    </div>
                </div>

                <!-- Campo de Entrada -->
                <div class="input-container-agnos">
                    <div class="input-icon-agnos">
                        <i data-lucide="link"></i>
                    </div>
                    <input type="text" id="video-url" placeholder="Pega la dirección de tu video..." required autocomplete="off">
                    <button class="btn-paste-agnos" onclick="pasteFromClipboard()">
                        <i data-lucide="clipboard" style="width: 14px; height: 14px;"></i> Pegar
                    </button>
                </div>

                <!-- Botón Buscar -->
                <button class="btn-submit-agnos" id="btn-submit" onclick="fetchVideoInfo()">
                    <i data-lucide="sparkles"></i> Buscar y Preparar
                </button>

                <!-- Caja de Mensajes -->
                <div class="message-box-agnos" id="message-box"></div>

                <!-- Loader Spinner -->
                <div class="status-container-agnos" id="status-container">
                    <div class="spinner-outer-agnos"></div>
                    <div class="status-text-agnos" id="status-text">Procesando enlace...</div>
                    <div class="status-sub-agnos" id="status-sub">Analizando formatos y tamaños disponibles</div>
                    <div class="pulse-bar-container-agnos">
                        <div class="pulse-bar-agnos"></div>
                    </div>
                </div>

                <!-- Tarjeta de Resultados -->
                <div class="preview-card-agnos" id="preview-card">
                    <div class="preview-content-agnos">
                        <div class="thumbnail-container-agnos">
                            <img src="" alt="Miniatura" class="thumbnail-img-agnos" id="preview-thumb">
                        </div>
                        <div class="video-details-agnos">
                            <div class="video-title-agnos" id="preview-title">Título de Video</div>
                            <div class="video-meta-agnos">
                                <div class="meta-badge-agnos">
                                    <i data-lucide="user"></i>
                                    <span id="preview-author">Creador</span>
                                </div>
                                <div class="meta-badge-agnos">
                                    <i data-lucide="clock"></i>
                                    <span id="preview-duration">00:00</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Selector de Pestañas -->
                    <div class="format-tabs-agnos">
                        <button class="tab-btn-agnos active" id="tab-video" onclick="switchTab('video')">Video (MP4)</button>
                        <button class="tab-btn-agnos" id="tab-audio" onclick="switchTab('audio')">Audio (MP3/M4A)</button>
                    </div>

                    <!-- Listado de Calidades -->
                    <div class="format-list-agnos active" id="video-formats-list"></div>
                    <div class="format-list-agnos" id="audio-formats-list"></div>
                </div>
            </div>
            
            <!-- Boceto Anotación Caveat -->
            <div class="framer-zl46kq" style="position: absolute; right: -150px; top: 10px; display: flex; align-items: center; gap: 10px; pointer-events: none; z-index:15;">
                <div style="width: 32px; height: 31px; transform: scaleX(-1) rotate(20deg); opacity: 0.85;">
                    <img src="https://framerusercontent.com/images/70A1TVDytyaXNukzYYdKPABwt1c.svg" alt="Arrow" style="width: 100%; height: 100%;">
                </div>
                <div style="font-family: 'Caveat', cursive; font-size: 1.8rem; color: #ff6321; white-space: nowrap; transform: rotate(-5deg); text-shadow: 0 0 10px rgba(255, 99, 33, 0.1);">
                    ¡100% Rápido y HD! ✨
                </div>
            </div>
        </div>
    </div>"""

    # Encontramos la sección que contiene los botones y la reemplazamos con nuestro descargador
    # Buscamos desde <div class="framer-1xk51t1" data-framer-name="Buttons"> hasta el siguiente div del nivel correspondiente
    # Hacemos un reemplazo simple aprovechando que localizamos el inicio de la etiqueta de botones
    
    # Para hacerlo sumamente preciso, reemplazaremos el bloque que contiene el botón "Discuss your ideas", "View services" y su estructura externa
    # El bloque original de botones en template_web_3d.txt va desde:
    # <div class="framer-1xk51t1" data-framer-name="Buttons"> hasta justo antes del bloque "Trusted by"
    # que es <div class="framer-zl46kq hidden-s5n491" ...> y <div class="framer-89snd1" data-framer-name="Bottom">
    
    # Buscamos la firma exacta de los botones en la línea 158:
    buttons_pattern = r'<div class="framer-1xk51t1" data-framer-name="Buttons">.*?</div></div></div></div><div class="framer-89snd1"'
    # Reemplazamos conservando la sección Bottom
    match = re.search(buttons_pattern, html)
    if match:
        print("Bloque de botones original localizado con regex exitosamente.")
        html = re.sub(buttons_pattern, downloader_html + '<div class="framer-89snd1"', html)
    else:
        # Fallback simple si la regex falla por variaciones menores
        print("Regex de botones no coincidió, usando reemplazo simple de contenedor...")
        html = html.replace('<div class="framer-1xk51t1" data-framer-name="Buttons">', downloader_html + '<!--')

    # 5. Inyección de Hojas de Estilo en la Cabecera
    # Buscaremos '</head>' e inyectaremos nuestro CSS personalizado
    custom_styles = """
    <!-- Lucide Icons & Google Fonts for Downloader -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Geist:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- GSAP for interactive animations -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

    <style>
        .flowget-downloader-wrapper {
            margin-top: 40px !important;
            position: relative;
            z-index: 25;
            width: 100%;
        }

        .downloader-card-glass {
            background: rgba(6, 6, 18, 0.45) !important;
            backdrop-filter: blur(35px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(35px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 24px !important;
            padding: 30px !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05),
                        0 0 40px rgba(255, 99, 33, 0.03) !important;
            position: relative;
            z-index: 10;
            overflow: hidden;
        }

        /* Spotlight tracking aura */
        .downloader-spotlight {
            position: absolute;
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(255, 99, 33, 0.16) 0%, rgba(99, 102, 241, 0.06) 50%, transparent 100%);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 1;
            border-radius: 50%;
            mix-blend-mode: screen;
            transition: opacity 0.4s ease;
            opacity: 0;
        }

        .flowget-downloader-wrapper:hover .downloader-spotlight {
            opacity: 1;
        }

        .platform-grid-agnos {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-bottom: 24px;
            position: relative;
            z-index: 5;
        }

        .platform-item-agnos {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 10px 4px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 6px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .platform-item-agnos i, .platform-item-agnos svg {
            width: 18px;
            height: 18px;
            color: #69686e;
            transition: color 0.25s ease;
        }

        .platform-item-agnos span {
            font-size: 0.72rem;
            font-weight: 500;
            color: #69686e;
            font-family: 'Geist', sans-serif;
            transition: color 0.25s ease;
        }

        .platform-item-agnos:hover {
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.12);
        }

        .platform-item-agnos[data-platform="youtube"]:hover i,
        .platform-item-agnos[data-platform="youtube"]:hover span { color: #ff3b30; }
        .platform-item-agnos[data-platform="tiktok"]:hover svg,
        .platform-item-agnos[data-platform="tiktok"]:hover span { color: #00f2fe; }
        .platform-item-agnos[data-platform="instagram"]:hover i,
        .platform-item-agnos[data-platform="instagram"]:hover span { color: #ec4899; }
        .platform-item-agnos[data-platform="twitter"]:hover i,
        .platform-item-agnos[data-platform="twitter"]:hover span { color: #ffffff; }
        .platform-item-agnos[data-platform="facebook"]:hover i,
        .platform-item-agnos[data-platform="facebook"]:hover span { color: #1877f2; }

        .input-container-agnos {
            display: flex;
            align-items: center;
            background: rgba(6, 6, 18, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 6px;
            margin-bottom: 16px;
            position: relative;
            z-index: 5;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .input-container-agnos:focus-within {
            border-color: #ff6321;
            box-shadow: 0 0 15px rgba(255, 99, 33, 0.12);
        }

        .input-icon-agnos {
            padding: 0 12px;
            color: #69686e;
            display: flex;
            align-items: center;
        }

        .input-container-agnos input[type="text"] {
            flex-grow: 1;
            width: 100%;
            background: transparent;
            border: none;
            outline: none;
            padding: 10px 0;
            color: #fff;
            font-size: 0.92rem;
            font-family: 'Geist', sans-serif;
        }

        .btn-paste-agnos {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #faf9f8;
            padding: 8px 14px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.78rem;
            font-family: 'Geist', sans-serif;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }

        .btn-paste-agnos:hover {
            background: rgba(255, 99, 33, 0.15);
            border-color: #ff6321;
            color: #ff6321;
        }

        .btn-submit-agnos {
            width: 100%;
            background: #ff6321;
            color: #fff;
            border: none;
            padding: 14px;
            font-size: 0.95rem;
            font-weight: 700;
            font-family: 'Geist', sans-serif;
            border-radius: 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 6px 20px rgba(255, 99, 33, 0.25);
            position: relative;
            z-index: 5;
            transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .btn-submit-agnos:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(255, 99, 33, 0.4);
            filter: brightness(1.05);
        }

        .btn-submit-agnos:active {
            transform: scale(0.98);
        }

        .message-box-agnos {
            display: none;
            margin-top: 14px;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.82rem;
            font-weight: 500;
            font-family: 'Geist', sans-serif;
            align-items: center;
            gap: 8px;
            position: relative;
            z-index: 5;
            animation: fadeIn 0.3s ease;
        }

        .message-box-agnos.error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }

        .message-box-agnos.success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #10b981;
        }

        .status-container-agnos {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: rgba(6, 6, 18, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            text-align: center;
            position: relative;
            z-index: 5;
        }

        .spinner-outer-agnos {
            width: 36px;
            height: 36px;
            border: 3px solid rgba(255, 255, 255, 0.05);
            border-radius: 50%;
            border-top-color: #ff6321;
            border-right-color: #6366f1;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 12px;
        }

        .status-text-agnos {
            font-size: 0.88rem;
            font-weight: 600;
            color: #faf9f8;
            font-family: 'Geist', sans-serif;
            margin-bottom: 4px;
        }

        .status-sub-agnos {
            font-size: 0.75rem;
            color: #69686e;
            font-family: 'Geist', sans-serif;
        }

        .pulse-bar-container-agnos {
            width: 100%;
            height: 3px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 12px;
        }

        .pulse-bar-agnos {
            width: 50%;
            height: 100%;
            background: linear-gradient(90deg, transparent, #ff6321, #6366f1, transparent);
            animation: pulse-move 1.4s infinite linear;
        }

        .preview-card-agnos {
            display: none;
            margin-top: 24px;
            background: rgba(6, 6, 18, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 16px;
            position: relative;
            z-index: 5;
            animation: slideDown 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .preview-content-agnos {
            display: flex;
            gap: 14px;
            margin-bottom: 16px;
            align-items: center;
        }

        .thumbnail-container-agnos {
            flex-shrink: 0;
            width: 100px;
            height: 60px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .thumbnail-img-agnos {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .video-details-agnos {
            flex-grow: 1;
        }

        .video-title-agnos {
            font-size: 0.88rem;
            font-weight: 600;
            line-height: 1.3;
            color: #faf9f8;
            margin-bottom: 4px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-align: left;
        }

        .video-meta-agnos {
            display: flex;
            gap: 6px;
            font-size: 0.72rem;
            color: #69686e;
        }

        .meta-badge-agnos {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            padding: 2px 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .meta-badge-agnos svg {
            width: 10px;
            height: 10px;
        }

        .format-tabs-agnos {
            display: flex;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 14px;
        }

        .tab-btn-agnos {
            flex: 1;
            background: none;
            border: none;
            padding: 10px;
            font-family: 'Geist', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: #69686e;
            cursor: pointer;
            position: relative;
            transition: color 0.2s ease;
        }

        .tab-btn-agnos.active {
            color: #ff6321;
        }

        .tab-btn-agnos.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 2px;
            background: #ff6321;
            border-radius: 100px;
        }

        .format-list-agnos {
            display: none;
            flex-direction: column;
            gap: 8px;
            max-height: 220px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .format-list-agnos.active {
            display: flex;
        }

        .format-row-agnos {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 10px 14px;
            transition: all 0.2s ease;
        }

        .format-row-agnos:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.08);
        }

        .format-info-agnos {
            display: flex;
            align-items: center;
            gap: 10px;
            text-align: left;
        }

        .format-icon-agnos {
            color: #ff6321;
            display: flex;
            align-items: center;
        }

        .format-details-agnos {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }

        .format-lbl-agnos {
            font-size: 0.8rem;
            font-weight: 600;
            color: #faf9f8;
        }

        .format-size-agnos {
            font-size: 0.72rem;
            color: #69686e;
        }

        .btn-row-dl-agnos {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #faf9f8;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'Geist', sans-serif;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: all 0.2s ease;
        }

        .btn-row-dl-agnos:hover {
            background: #ff6321;
            border-color: #ff6321;
            color: #fff;
            box-shadow: 0 4px 10px rgba(255, 99, 33, 0.25);
        }

        .btn-row-dl-agnos:active {
            transform: scale(0.96);
        }

        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulse-move {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(200%); }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media(max-width: 680px) {
            .platform-grid-agnos { grid-template-columns: repeat(3, 1fr); }
            .platform-item-agnos:nth-child(4), .platform-item-agnos:nth-child(5) { grid-column: span 1; }
            .downloader-card-glass { padding: 20px 16px !important; }
        }
    </style>
    """
    html = html.replace("</head>", custom_styles + "\n</head>")

    # 6. Inyección de JavaScript en el pie de página
    # Buscaremos '</body>' e inyectaremos nuestro script dinámico AJAX y GSAP
    custom_scripts = """
    <script>
        // Initialize Lucide Icons
        lucide.createIcons();

        // 3D Spotlight mouse follower within the Downloader
        const dlWrapper = document.querySelector('.flowget-downloader-wrapper');
        const dlSpotlight = document.getElementById('dl-spotlight');

        if (dlWrapper && dlSpotlight) {
            dlWrapper.addEventListener('mousemove', (e) => {
                const rect = dlWrapper.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                gsap.to(dlSpotlight, {
                    left: x,
                    top: y,
                    duration: 0.1,
                    ease: "power2.out"
                });
            });
        }

        // Downloader Logic & Endpoints
        const videoUrlInput = document.getElementById('video-url');
        const btnSubmit = document.getElementById('btn-submit');
        const statusContainer = document.getElementById('status-container');
        const statusText = document.getElementById('status-text');
        const statusSub = document.getElementById('status-sub');
        const messageBox = document.getElementById('message-box');
        const previewCard = document.getElementById('preview-card');

        let currentProcessedUrl = '';
        let optionsList = [];

        async function pasteFromClipboard() {
            try {
                if (navigator.clipboard && navigator.clipboard.readText) {
                    const text = await navigator.clipboard.readText();
                    if (text) {
                        videoUrlInput.value = text;
                        showMessage("Enlace pegado correctamente del portapapeles.", "success");
                        setTimeout(() => hideMessage(), 2500);
                    } else {
                        showMessage("El portapapeles está vacío.", "error");
                    }
                } else {
                    showMessage("Clipboard API no soportada en este navegador.", "error");
                }
            } catch (err) {
                showMessage("Permiso de portapapeles denegado.", "error");
            }
        }

        function suggestPlatform(name) {
            showMessage(`Listo para procesar enlaces de ${name}. Pega el enlace arriba.`, "success");
            videoUrlInput.focus();
            setTimeout(() => hideMessage(), 3000);
        }

        function showMessage(text, type) {
            messageBox.innerText = text;
            messageBox.className = `message-box-agnos ${type}`;
            messageBox.style.display = 'flex';
        }

        function hideMessage() {
            messageBox.style.display = 'none';
        }

        function switchTab(type) {
            document.getElementById('tab-video').classList.toggle('active', type === 'video');
            document.getElementById('tab-audio').classList.toggle('active', type === 'audio');
            
            document.getElementById('video-formats-list').classList.toggle('active', type === 'video');
            document.getElementById('audio-formats-list').classList.toggle('active', type === 'audio');
        }

        function fetchVideoInfo() {
            const url = videoUrlInput.value.trim();
            if (!url) {
                showMessage("Por favor, ingresa una URL válida.", "error");
                return;
            }

            previewCard.style.display = 'none';
            hideMessage();

            // Enable loader using GSAP transitions
            statusContainer.style.display = 'block';
            statusText.innerText = "Analizando enlace...";
            statusSub.innerText = "Consultando formatos de video y audio con el servidor...";
            btnSubmit.disabled = true;

            gsap.fromTo(statusContainer, { scale: 0.96, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "power2.out" });

            fetch('/get_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message || 'Error en el servidor'); });
                }
                return response.json();
            })
            .then(data => {
                statusContainer.style.display = 'none';
                btnSubmit.disabled = false;

                if (data.success) {
                    currentProcessedUrl = data.original_url;
                    optionsList = data.options;

                    // Set preview card values
                    document.getElementById('preview-thumb').src = data.thumbnail || 'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=3540&auto=format&fit=crop';
                    document.getElementById('preview-title').innerText = data.title;
                    document.getElementById('preview-author').innerText = data.uploader;
                    document.getElementById('preview-duration').innerText = data.duration;

                    // Render list
                    renderFormats(data.options);

                    // Show preview card using GSAP
                    previewCard.style.display = 'block';
                    gsap.fromTo(previewCard, { scale: 0.95, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.2)" });
                    
                    switchTab('video');
                    showMessage("Formatos extraídos con éxito. Selecciona la opción que deseas descargar.", "success");
                } else {
                    showMessage(data.message || "No se pudo obtener información del enlace.", "error");
                }
            })
            .catch(error => {
                statusContainer.style.display = 'none';
                btnSubmit.disabled = false;
                showMessage(error.message || "Error al conectar con el servidor de descargas.", "error");
            });
        }

        function renderFormats(options) {
            const videoList = document.getElementById('video-formats-list');
            const audioList = document.getElementById('audio-formats-list');

            videoList.innerHTML = '';
            audioList.innerHTML = '';

            options.forEach(opt => {
                const row = document.createElement('div');
                row.className = 'format-row-agnos';
                
                const isVideo = opt.type === 'video';
                const icon = isVideo ? 'video' : 'music';

                row.innerHTML = `
                    <div class="format-info-agnos">
                        <div class="format-icon-agnos">
                            <i data-lucide="${icon}"></i>
                        </div>
                        <div class="format-details-agnos">
                            <div class="format-lbl-agnos">${opt.label}</div>
                            <div class="format-size-agnos"><i data-lucide="hard-drive" style="width: 10px; height: 10px; display: inline; vertical-align: middle; margin-right: 2px;"></i> Peso: ${opt.size}</div>
                        </div>
                    </div>
                    <button class="btn-row-dl-agnos" onclick="downloadFile('${opt.id}', '${opt.label}')">
                        <i data-lucide="download"></i> Descargar
                    </button>
                `;

                if (isVideo) {
                    videoList.appendChild(row);
                } else {
                    audioList.appendChild(row);
                }
            });

            // Re-render lucide icons inside rows
            lucide.createIcons();
        }

        function downloadFile(optionId, label) {
            if (!currentProcessedUrl) {
                showMessage("No hay un video analizado.", "error");
                return;
            }

            previewCard.style.display = 'none';
            hideMessage();

            // Enable loader
            statusContainer.style.display = 'block';
            statusText.innerText = "Procesando descarga...";
            statusSub.innerText = `Descargando y convirtiendo en el servidor: "${label}"...`;
            
            gsap.fromTo(statusContainer, { scale: 0.96, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "power2.out" });

            fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: currentProcessedUrl,
                    option_id: optionId
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message || 'Error al descargar'); });
                }
                return response.json();
            })
            .then(data => {
                statusContainer.style.display = 'none';
                previewCard.style.display = 'block';

                if (data.success && data.filename) {
                    showMessage("¡Conversión exitosa! Transfiriendo archivo a tu almacenamiento...", "success");
                    window.location.href = `/serve_file/${encodeURIComponent(data.filename)}`;
                } else {
                    showMessage(data.message || "Error al procesar el formato seleccionado.", "error");
                }
            })
            .catch(error => {
                statusContainer.style.display = 'none';
                previewCard.style.display = 'block';
                showMessage(error.message || "Error al descargar el archivo.", "error");
            });
        }
    </script>
    """
    html = html.replace("</body>", custom_scripts + "\n</body>")

    print(f"Escribiendo resultado integrado en: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Integración completada exitosamente. templates/index.html generado.")

if __name__ == "__main__":
    integrate()
