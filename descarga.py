import streamlit as st
from pytube import YouTube
from pytube.cli import on_progress

def download_video(url, st_progress):
    try:
        yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: update_progress(stream, bytes_remaining, st_progress))
        video = yt.streams.get_highest_resolution()
        video.download()
        st_progress.text(f"Descargado: {video.title}")
    except Exception as e:
        st_progress.text(f"Error descargando {url}: {str(e)}")

def update_progress(stream, bytes_remaining, st_progress):
    total_size = stream.filesize
    percent_complete = 100 - (bytes_remaining / total_size * 100)
    st_progress.text(f"Descargando: {stream.title} - {percent_complete:.2f}% completado.")

def main():
    st.title('Descargador de videos de YouTube')
    
    # Caja de texto para múltiples URLs
    urls = st.text_area("Ingresa las URLs de los videos de YouTube, separadas por saltos de línea:", height=300)
    
    # Botón para iniciar la descarga
    if st.button('Descargar videos'):
        if not urls:
            st.warning("Por favor, ingresa al menos un enlace de YouTube.")
        else:
            url_list = urls.split("\n")
            for url in url_list:
                if url.strip():
                    st_progress = st.empty()
                    download_video(url.strip(), st_progress)

if __name__ == "__main__":
    main()
