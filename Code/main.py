import streamlit as st
from summary import Summarizer
from evaluate import Evaluate
from nltk.tokenize import sent_tokenize
from pdfminer.high_level import extract_text
import docx
import requests
from bs4 import BeautifulSoup
from readURL import FrequencySummarizer


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_model():
    s = Summarizer()
    e = Evaluate()
    return s, e


def getFileExtension(filenam):
    arr1 = filenam.split('.')
    return arr1[len(arr1)-1]


def readDocFile(filenam):
    doc = docx.Document(filenam)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def readPdfFile(filenam):
    all_text = extract_text(filenam)
    return all_text


def getTextFromURL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ""

    if "soha" in url:  # Báo Soha
        main_text = soup.find('main')
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "vietnamnet" in url:  # Báo Vietnamnet
        main_text = soup.find(attrs={"id": "ArticleContent"})
        text = ' '.join(map(lambda p: p.text, main_text.find_all("p", "t-j")))
    elif "zingnews" in url:
        # Thử báo Zing news
        main_text = soup.find(attrs={"class": "the-article-body"})
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "vnexpress" in url:
        # Thử báo vnexpress
        main_text = soup.find(attrs={"class": "sidebar-1"})
        text = ' '.join(map(lambda p: p.text if not p.has_attr(
            "style") else "", main_text.find_all('p')))
    elif "thanhnien" in url:
        main_text = soup.find(attrs={"id": "abody"})  # Thử báo thanh niên
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "dantri" in url:
        main_text = soup.find(
            attrs={"class": "singular-content"})  # Thử báo dân trí
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "nld.com.vn" in url:
        # Thử báo người lao động
        main_text = soup.find(attrs={"class": "content-news-detail old-news"})
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "laodong.vn" in url:
        main_text = soup.find(
            attrs={"class": "article-content"})  # Thử báo lao động
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "baotintuc.vn" in url:
        main_text = soup.find(attrs={"class": "contents"})  # Thử báo tin tức
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "docbao.vn" in url:
        main_text = soup.find(
            attrs={"class": "detail_content"})  # Thử báo đọc báo
        text = ' '.join(map(lambda p: p.text if not p.has_attr(
            "style") else "", main_text.find_all('p')))
    elif "www.24h.com.vn" in url:
        main_text = soup.find(
            attrs={"class": "cate-24h-foot-arti-deta-info"})  # Thử báo 24h
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "www.baohaiphong.com.vn" in url:
        main_text = soup.find(attrs={"class": "tmargin"})  # Thử báo Hải Phòng
        text = ' '.join(map(lambda p: p.text if not p.has_attr(
            "style") else "", main_text.find_all('p')))
    elif "nhandan.vn" in url:
        main_text = soup.find(
            attrs={"class": "detail-content-body"})  # Thử báo nhân dân
        text = ' '.join(map(lambda p: p.text, main_text.find_all('p')))
    elif "tuoitre.vn" in url:
        main_text = soup.find(
            attrs={"class": "content fck"})  # Thử báo tuổi trẻ
        text = ' '.join(map(lambda p: p.text if not p.has_attr(
            "data-placeholder") else "", main_text.find_all('p')))

    sents = sent_tokenize(text.replace("\n", " "))
    return " ".join(sents)


summarizer, evaluate = load_model()
st.title("TÓM TẮT VĂN BẢN TIẾNG VIỆT BẰNG PHƯƠNG PHÁP MACHINE LEARNING")
full_text = st.text_area(
    "Nhập đoạn văn bản hoặc đường dẫn đến trang web muốn tóm tắt!")
st.session_state.catch_rand = full_text
uploaded_file = st.file_uploader("Chọn file muốn tóm tắt (PDF, DOC, DOCX)")
if uploaded_file is not None:
    ex = getFileExtension(uploaded_file.name)
    if "doc" in ex:
        full_text = readDocFile(uploaded_file)
    elif "pdf" in ex:
        full_text = readPdfFile(uploaded_file)
    st.write(full_text)

if full_text[0:8] == "https://":
    full_text = str(getTextFromURL(full_text))


options = ["Clustering", "LSA", "TextRank"]
choice = st.selectbox("Lựa chọn thuật toán", options)
if st.button("Tóm tắt"):
    if choice == options[0]:
        summary = summarizer.summarize(full_text)
    elif choice == options[1]:
        summary = summarizer.summarize(full_text, mode="lsa")
    else:
        summary = summarizer.summarize(full_text, mode="text rank")
    score = evaluate.content_based(summary[0], full_text)
    st.write(summary[0])
    st.write("-"*20)
    list_sentence_selected = list(summary[1])
    list_sentence_selected = list(map(str, list_sentence_selected))

    st.write("Các câu đã lựa chọn: ${}$".format(
        ", ".join(list_sentence_selected)))
    st.write(
        "Với {:.2f}% thông tin được giữ lại (Đánh giá dựa trên nội dung!)".format(score*100))
