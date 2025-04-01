import os
import sys
import re
import yt_dlp
import html
import argparse

def limpar_texto(texto):
    """
    Remove formatações HTML e caracteres especiais do texto.
    """
    # Remove tags HTML
    texto = re.sub(r'<[^>]+>', '', texto)
    # Decodifica entidades HTML
    texto = html.unescape(texto)
    # Remove múltiplos espaços em branco
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def extrair_legendas(url, idioma='pt', escrever_arquivo=True):
    """
    Extrai legendas (closed captions) de um vídeo do YouTube.
    
    Args:
        url: URL do vídeo do YouTube
        idioma: código de idioma (pt, en, es, etc.)
        escrever_arquivo: se True, salva as legendas em um arquivo
        
    Returns:
        Texto das legendas ou mensagem de erro
    """
    try:
        print(f"Extraindo legendas do vídeo: {url}")
        print(f"Idioma desejado: {idioma}")
        
        # Configurações para o yt-dlp
        ydl_opts = {
            'skip_download': True,  # Não baixa o vídeo
            'writesubtitles': True,  # Habilita download de legendas
            'writeautomaticsub': True,  # Habilita download de legendas automáticas
            'subtitleslangs': [idioma],  # Idioma desejado
            'quiet': False,
            'no_warnings': False
        }
        
        # Primeira tentativa: extrair informações do vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            titulo = info.get('title', 'video')
            titulo_seguro = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in titulo).strip()
            
            # Verifica se há legendas disponíveis
            legendas_disponiveis = info.get('subtitles', {})
            legendas_auto = info.get('automatic_captions', {})
            
            print("\nLegendas disponíveis:")
            for idioma_disp in legendas_disponiveis:
                print(f" - {idioma_disp} (manual)")
            
            for idioma_auto in legendas_auto:
                print(f" - {idioma_auto} (automática)")
            
            # Tenta baixar as legendas
            temp_dir = os.getcwd()
            
            # Configurações para download apenas das legendas
            ydl_opts_download = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': [idioma],
                'subtitlesformat': 'ttml',  # Formato que preserva o texto completo
                'outtmpl': os.path.join(temp_dir, 'legendas_temp'),
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
                ydl_download.download([url])
            
            # Procura pelo arquivo de legendas gerado
            arquivo_legendas = None
            for arquivo in os.listdir(temp_dir):
                if arquivo.startswith('legendas_temp') and (
                    f'.{idioma}.' in arquivo or 
                    f'.{idioma}-auto.' in arquivo
                ):
                    arquivo_legendas = os.path.join(temp_dir, arquivo)
                    break
            
            if not arquivo_legendas:
                # Tenta com idioma alternativo (pt-BR, en-US, etc.)
                for arquivo in os.listdir(temp_dir):
                    if arquivo.startswith('legendas_temp') and (
                        f'.{idioma}' in arquivo or 
                        idioma in arquivo
                    ):
                        arquivo_legendas = os.path.join(temp_dir, arquivo)
                        break
            
            if not arquivo_legendas:
                return f"Não foi possível encontrar legendas no idioma '{idioma}'. Tente outro idioma (en, es, fr, etc.)"
            
            # Lê o arquivo de legendas
            with open(arquivo_legendas, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Extrai o texto das legendas
            texto_legendas = ""
            
            # TTML format
            if arquivo_legendas.endswith('.ttml'):
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(conteudo)
                    # Extrai texto dos elementos <p>
                    for elem in root.findall(".//{http://www.w3.org/ns/ttml}p"):
                        linha = ''.join(elem.itertext())
                        texto_legendas += limpar_texto(linha) + "\n"
                except:
                    # Fallback para regex se o parsing XML falhar
                    matches = re.findall(r'<p[^>]*>(.*?)</p>', conteudo, re.DOTALL)
                    for match in matches:
                        texto_legendas += limpar_texto(match) + "\n"
            
            # VTT format
            elif arquivo_legendas.endswith('.vtt'):
                # Pula o cabeçalho
                linhas = conteudo.split('\n')
                for i, linha in enumerate(linhas):
                    # Ignora o cabeçalho, timestamps e linhas vazias
                    if '-->' in linha or not linha.strip() or i < 2:
                        continue
                    # Ignora números de sequência
                    if linha.strip().isdigit():
                        continue
                    texto_legendas += limpar_texto(linha) + "\n"
            
            # Formato SRT
            elif arquivo_legendas.endswith('.srt'):
                # Remove números e timestamps
                texto_limpo = re.sub(r'\d+\s*\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*\n', '\n', conteudo)
                for linha in texto_limpo.split('\n'):
                    if linha.strip():
                        texto_legendas += limpar_texto(linha) + "\n"
            
            # XML ou outro formato
            else:
                # Tenta extrair texto de qualquer tag
                texto_legendas = limpar_texto(conteudo)
            
            # Remove linhas duplicadas consecutivas
            linhas = texto_legendas.split('\n')
            texto_final = ""
            ultima_linha = None
            
            for linha in linhas:
                linha = linha.strip()
                if linha and linha != ultima_linha:
                    texto_final += linha + "\n"
                    ultima_linha = linha
            
            # Salva em arquivo se solicitado
            if escrever_arquivo:
                nome_arquivo = f"transcricao_{titulo_seguro[:50]}_{idioma}.txt"
                with open(nome_arquivo, 'w', encoding='utf-8') as f:
                    f.write(texto_final)
                print(f"\nTranscrição salva em: {nome_arquivo}")
            
            # Remove o arquivo temporário de legendas
            try:
                os.remove(arquivo_legendas)
            except:
                pass
            
            return texto_final
            
    except Exception as e:
        return f"Erro ao extrair legendas: {str(e)}"

def main():
    # Configuração dos argumentos
    parser = argparse.ArgumentParser(description='Extrai legendas de vídeos do YouTube')
    parser.add_argument('url', help='URL do vídeo do YouTube')
    parser.add_argument('-i', '--idioma', default='pt', help='Código do idioma (pt, en, es, etc.)')
    parser.add_argument('-nl', '--no-log', action='store_true', help='Não salvar em arquivo')
    
    # Parse args se houver, ou use sys.argv
    if len(sys.argv) > 1:
        args = parser.parse_args()
        url = args.url
        idioma = args.idioma
        salvar = not args.no_log
    else:
        url = input("Digite a URL do vídeo do YouTube: ")
        idioma = input("Digite o código do idioma (pt, en, es, etc.) [padrão: pt]: ") or "pt"
        salvar = True
    
    # Extrai as legendas
    texto = extrair_legendas(url, idioma, salvar)
    
    # Exibe o resultado
    print("\nTexto extraído:")
    print("-" * 50)
    print(texto)
    print("-" * 50)

if __name__ == "__main__":
    main()