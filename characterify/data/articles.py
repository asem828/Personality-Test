from __future__ import annotations

"""Learn module content.

Requirements:
 - 25 articles
 - Each article content is >= ~200 words (ID & EN versions)
 - Stored as static data (offline-first)

Notes:
 - Content is educational and non-clinical.
 - Rendered with QTextBrowser (HTML).
"""

from typing import Dict, List


def _word_count_html(html: str) -> int:
    import re

    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-zA-Z0-9#]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return 0 if not text else len(text.split(" "))


def _augment_if_short(title: str, html: str, lang: str) -> str:

    if _word_count_html(html) >= 200:
        return html

    if lang == "en":
        extra = f"""
<h2>Practice & Reflection</h2>
<p><b>Make it actionable:</b> pick one idea from <i>{title}</i> and turn it into a small habit you can repeat for 7 days. Keep the habit tiny on purpose—consistency matters more than intensity.</p>
<ul>
  <li><b>One-sentence plan:</b> “When ___ happens, I will ___ for ___ minutes.”</li>
  <li><b>Friction check:</b> what usually blocks you (time, mood, environment)? Remove one obstacle.</li>
  <li><b>Scorecard:</b> after each day, rate (1–5) your energy, focus, and stress. Look for patterns.</li>
</ul>
<p><b>Reflection prompts:</b> What did you learn about your defaults? Which situation amplified your strengths—and which one triggered your blind spot? Write a short note so the insight becomes reusable, not just a “nice read.”</p>
<p><i>Reminder:</i> this content is educational and not a clinical diagnosis. If distress or anxiety feels heavy and persistent, consider talking with a qualified professional.</p>
"""
    else:
        extra = f"""
<h2>Latihan & Refleksi</h2>
<p><b>Buat jadi nyata:</b> pilih satu ide dari <i>{title}</i> lalu ubah menjadi kebiasaan kecil selama 7 hari. Sengaja dibuat kecil agar mudah konsisten—stabilitas lebih penting daripada intensitas.</p>
<ul>
  <li><b>Rencana 1 kalimat:</b> “Saat ___ terjadi, saya akan ___ selama ___ menit.”</li>
  <li><b>Cek hambatan:</b> apa yang biasanya menghalangi (waktu, mood, lingkungan)? Hilangkan 1 hambatan.</li>
  <li><b>Skor harian:</b> setelah menjalankan, nilai (1–5) energi, fokus, dan stres. Cari polanya.</li>
</ul>
<p><b>Pertanyaan refleksi:</b> Apa yang Anda pelajari tentang pola otomatis Anda? Situasi apa yang memperkuat kekuatan Anda—dan situasi apa yang memicu blind spot? Catat singkat agar insight bisa dipakai ulang.</p>
<p><i>Catatan:</i> konten ini bersifat edukatif dan bukan diagnosis klinis. Jika stres atau kecemasan terasa berat dan berkepanjangan, pertimbangkan berdiskusi dengan profesional.</p>
"""

    return html + "\n" + extra


ARTICLES: List[Dict] = [
    {
        "id": "a01",
        "title_id": "Apa itu Kepribadian? Panduan Singkat dan Netral",
        "title_en": "What Is Personality? A Short, Neutral Guide",
        "category_id": "Dasar",
        "category_en": "Fundamentals",
        "read_time": "8 min",
        "summary_id": "Definisi kepribadian, bedanya trait vs state, dan cara memakai tes secara etis.",
        "summary_en": "A practical definition, trait vs state, and how to use tests ethically.",
        "content_id": """
<h2>Gambaran Umum</h2>
<p>Dalam psikologi, <b>kepribadian</b> adalah pola kecenderungan yang relatif konsisten dalam cara seseorang berpikir, merasakan, dan bertindak. Kata kuncinya adalah <i>pola</i> dan <i>kecenderungan</i>: kepribadian bukan berarti Anda akan selalu bertindak sama di setiap situasi, tetapi ada gaya yang sering muncul ketika Anda menghadapi keputusan, relasi, tekanan, dan rutinitas.</p>

<h2>Trait vs State</h2>
<p>Anda akan sering menemukan istilah <b>trait</b> dan <b>state</b>. Trait adalah kecenderungan jangka panjang (misalnya teliti, ekspresif, atau mudah cemas). State adalah kondisi sementara (misalnya lelah, stres, antusias). Seseorang dengan trait “tenang” tetap bisa mengalami state “cemas” ketika deadline menumpuk. Karena itu, menilai diri hanya dari satu hari yang berat sering menyesatkan.</p>

<h2>Bagaimana Tes Dipakai Secara Sehat</h2>
<ul>
  <li><b>Refleksi diri</b>: temukan pola kekuatan, pemicu stres, dan blind spot.</li>
  <li><b>Komunikasi</b>: pahami perbedaan gaya kerja dan gaya berinteraksi dalam tim.</li>
  <li><b>Pengembangan</b>: ubah insight menjadi kebiasaan kecil yang konsisten.</li>
</ul>

<h2>3 Pertanyaan Refleksi</h2>
<ol>
  <li>Kapan saya merasa paling “hidup” dan produktif?</li>
  <li>Situasi apa yang paling cepat menguras energi saya?</li>
  <li>Kebiasaan kecil apa yang bisa saya latih minggu ini untuk menyeimbangkan diri?</li>
</ol>

<p><b>Catatan penting</b>: tes kepribadian bukan diagnosis klinis. Gunakan hasil sebagai alat bantu untuk memahami diri, bukan label permanen yang membatasi.</p>
""",
        "content_en": """
<h2>Overview</h2>
<p>In psychology, <b>personality</b> refers to relatively consistent patterns in how people think, feel, and behave. The key ideas are <i>patterns</i> and <i>tendencies</i>. Personality does not mean you will act the same way in every situation; it means certain styles often show up when you make decisions, build relationships, handle pressure, and manage routines.</p>

<h2>Trait vs State</h2>
<p>You will often see the terms <b>trait</b> and <b>state</b>. Traits are longer-term tendencies (for example: organized, expressive, or prone to worry). States are temporary conditions (for example: tired, stressed, excited). Someone with a generally calm trait can still experience an anxious state when deadlines pile up. That is why judging yourself based on a single hard week can be misleading.</p>

<h2>How to Use Tests in a Healthy Way</h2>
<ul>
  <li><b>Self-reflection</b>: identify strengths, stress triggers, and blind spots.</li>
  <li><b>Communication</b>: understand differences in work style and interaction style.</li>
  <li><b>Development</b>: turn insights into small, repeatable habits.</li>
</ul>

<h2>3 Reflection Prompts</h2>
<ol>
  <li>When do I feel most energized and productive?</li>
  <li>Which situations drain my energy the fastest?</li>
  <li>What small habit can I practice this week to balance myself?</li>
</ol>

<p><b>Important</b>: personality tests are not clinical diagnoses. Use results as guidance—not as a permanent label that limits growth.</p>
""",
    },
    {
        "id": "a02",
        "title_id": "Cara Membaca Hasil Tes dengan Bijak",
        "title_en": "How to Read Test Results Wisely",
        "category_id": "Dasar",
        "category_en": "Fundamentals",
        "read_time": "8 min",
        "summary_id": "Agar hasil tes jadi insight yang actionable, bukan label yang membatasi.",
        "summary_en": "Turn results into actionable insights—not limiting labels.",
        "content_id": """
<h2>Prinsip 1: Hasil itu Probabilistik</h2>
<p>Mayoritas tes kepribadian menggambarkan <b>kecenderungan</b>, bukan kepastian. Artinya: jika skor Anda tinggi pada suatu dimensi, Anda <i>lebih sering</i> menunjukkan perilaku tertentu, tetapi tetap ada variasi tergantung konteks, peran, dan kondisi emosional.</p>

<h2>Prinsip 2: Konteks Mengubah Perilaku</h2>
<p>Anda bisa terlihat “ekstrovert” di lingkungan aman, tetapi terlihat “introvert” ketika berada di tempat baru. Anda bisa sangat teliti di proyek yang Anda pedulikan, tetapi terlihat ceroboh ketika multitasking dan kurang tidur. Jangan menilai diri (atau orang lain) tanpa melihat konteks.</p>

<h2>Prinsip 3: Fokus pada Pola, Bukan Detail Kecil</h2>
<p>Jika hasil Anda “campuran” atau berada di tengah, itu normal. Gunakan hasil untuk menangkap <b>pola besar</b>: apa yang menguatkan Anda, apa yang cenderung melemahkan Anda, dan apa kebiasaan penyeimbang yang relevan.</p>

<h2>Langkah Praktis (10 Menit)</h2>
<ol>
  <li>Pilih <b>2–3 poin</b> yang paling terasa akurat.</li>
  <li>Tulis contoh nyata: <i>kapan</i> pola itu muncul?</li>
  <li>Ubah jadi eksperimen kecil: “Selama 7 hari, saya akan …”.</li>
  <li>Evaluasi: apa dampaknya pada energi, fokus, dan relasi?</li>
</ol>

<h2>Hal yang Perlu Dihindari</h2>
<ul>
  <li>Menggunakan hasil untuk menghakimi diri atau orang lain.</li>
  <li>Menganggap hasil sebagai alasan berhenti berkembang.</li>
  <li>Memaksakan semua keputusan besar berdasarkan satu tes.</li>
</ul>
""",
        "content_en": """
<h2>Principle 1: Results Are Probabilistic</h2>
<p>Most personality tests describe <b>tendencies</b>, not certainties. If you score high on a dimension, you will <i>more often</i> show certain behaviors—but you will still vary depending on context, role expectations, and emotional state.</p>

<h2>Principle 2: Context Shapes Behavior</h2>
<p>You may appear “extroverted” in a safe, familiar group and “introverted” in a brand‑new environment. You might be very conscientious on projects you care about, and much less so when you are sleep‑deprived and multitasking. Avoid judging yourself (or others) without considering context.</p>

<h2>Principle 3: Look for Patterns, Not Tiny Details</h2>
<p>Mixed or mid‑range results are common. Focus on the <b>big picture</b>: what energizes you, what tends to drain you, and what balancing habits could help.</p>

<h2>A 10‑Minute Practical Process</h2>
<ol>
  <li>Pick <b>2–3 points</b> that feel most accurate.</li>
  <li>Write real examples: <i>when</i> does this show up?</li>
  <li>Turn it into a small experiment: “For 7 days, I will …”.</li>
  <li>Review the impact on energy, focus, and relationships.</li>
</ol>

<h2>What to Avoid</h2>
<ul>
  <li>Using results to judge or label people.</li>
  <li>Treating results as an excuse to stop growing.</li>
  <li>Making every major life decision based on a single test.</li>
</ul>
""",
    },
    {
        "id": "a03",
        "title_id": "MBTI: Preferensi, Bukan Kemampuan",
        "title_en": "MBTI: Preferences, Not Ability",
        "category_id": "MBTI",
        "category_en": "MBTI",
        "read_time": "7 min",
        "summary_id": "Memahami MBTI sebagai preferensi (energi, informasi, keputusan, struktur), bukan ukuran pintar/kompeten.",
        "summary_en": "MBTI describes preferences (energy, information, decisions, structure), not intelligence or competence.",
        "content_id": """
<h2>MBTI Membahas “Cara Alami”, Bukan “Nilai”</h2>
<p>MBTI (Myers‑Briggs Type Indicator) mengelompokkan preferensi ke dalam 4 dimensi: <b>E/I</b> (sumber energi), <b>S/N</b> (cara memproses informasi), <b>T/F</b> (cara mengambil keputusan), dan <b>J/P</b> (cara mengatur hidup/kerja). MBTI tidak mengatakan tipe tertentu lebih cerdas, lebih baik, atau lebih layak memimpin.</p>

<h2>Mitos yang Sering Muncul</h2>
<ul>
  <li><b>“Tipe X pasti jago A.”</b> → Tidak selalu. Preferensi bukan keterampilan.</li>
  <li><b>“Saya introvert, berarti tidak bisa presentasi.”</b> → Anda bisa melatih keterampilan; hanya butuh strategi energi.</li>
  <li><b>“Kalau sudah tahu tipe, saya tidak perlu berubah.”</b> → Justru hasil tes membantu memilih area latihan yang relevan.</li>
</ul>

<h2>Penggunaan yang Produktif</h2>
<ol>
  <li><b>Kenali pemicu</b>: situasi apa yang membuat Anda cepat lelah atau cepat fokus?</li>
  <li><b>Bangun kebiasaan penyeimbang</b>: jika Anda condong ke satu sisi, latih “otot” sisi lain secara bertahap.</li>
  <li><b>Komunikasi tim</b>: gunakan MBTI sebagai bahasa untuk menyamakan ekspektasi (bukan untuk stereotip).</li>
</ol>

<h2>Pertanyaan Refleksi</h2>
<p>Jika Anda mengingat 2–3 keputusan besar terakhir, apakah Anda lebih banyak mengandalkan data dan logika, atau nilai dan dampak pada orang? Bagaimana hasil keputusan itu, dan apa yang ingin Anda perbaiki pada prosesnya?</p>
""",
        "content_en": """
<h2>MBTI Describes “Natural Style,” Not “Worth”</h2>
<p>MBTI (Myers‑Briggs Type Indicator) groups preferences into four dimensions: <b>E/I</b> (energy source), <b>S/N</b> (how you process information), <b>T/F</b> (how you decide), and <b>J/P</b> (how you structure work and life). MBTI does not claim that one type is smarter, better, or more fit to lead.</p>

<h2>Common Myths</h2>
<ul>
  <li><b>“Type X is automatically good at Y.”</b> → Not necessarily. Preferences are not skills.</li>
  <li><b>“I’m introverted, so I can’t present.”</b> → You can build the skill; you just need energy strategies.</li>
  <li><b>“Now that I know my type, I don’t need to change.”</b> → Results are most useful for choosing what to practice.</li>
</ul>

<h2>Productive Uses</h2>
<ol>
  <li><b>Identify triggers</b>: what situations drain you or help you focus quickly?</li>
  <li><b>Build balancing habits</b>: if you lean strongly one way, train the opposite “muscle” gradually.</li>
  <li><b>Team communication</b>: use MBTI as a shared language to align expectations (not to stereotype).</li>
</ol>

<h2>Reflection Prompt</h2>
<p>Think about your last 2–3 big decisions. Did you lean more on logic and criteria, or on values and human impact? What worked well—and what would you improve in your decision process next time?</p>
""",
    },

    # --- MBTI dimensions ---
    {
        "id": "a04",
        "title_id": "E vs I: Energi Sosial vs Energi Pribadi",
        "title_en": "E vs I: Social Energy vs Private Energy",
        "category_id": "MBTI",
        "category_en": "MBTI",
        "read_time": "8 min",
        "summary_id": "Cara mengenali sumber energi Anda dan strategi menjaga stamina sosial.",
        "summary_en": "How to recognize your energy source and protect social stamina.",
        "content_id": """
<h2>Intinya</h2>
<p><b>Extraversion (E)</b> cenderung mengisi ulang energi lewat interaksi, diskusi, dan stimulus dari luar. <b>Introversion (I)</b> cenderung pulih lewat waktu pribadi, fokus mendalam, dan stimulus yang lebih terkontrol. Ini bukan soal “suka orang” atau “anti sosial”—ini soal <i>cara recharge</i>.</p>

<h2>Contoh Situasi</h2>
<p>Dalam rapat panjang, E sering merasa ide mengalir saat berbicara. I bisa tetap aktif, tetapi membutuhkan jeda untuk memproses dan menyusun jawaban yang matang. Setelah acara sosial, E mungkin merasa lebih bersemangat, sementara I merasa perlu recovery.</p>

<h2>Strategi Praktis</h2>
<ul>
  <li><b>Jika Anda E</b>: buat blok fokus tanpa meeting agar tidak “kelebihan stimulus”. Siapkan catatan agar ide tetap terstruktur.</li>
  <li><b>Jika Anda I</b>: jadwalkan recovery time setelah meeting besar. Gunakan komunikasi tertulis untuk menyampaikan ide dengan tenang.</li>
  <li><b>Untuk keduanya</b>: gunakan ritme kerja <i>meeting → fokus → review</i> supaya energi stabil.</li>
</ul>

<h2>Latihan 7 Hari</h2>
<p>Selama seminggu, catat 2 hal: (1) aktivitas yang membuat energi naik, (2) aktivitas yang membuat energi turun. Lalu ubah kalender Anda: tambah 10–20% aktivitas “recharge” dan kurangi satu pemicu utama kelelahan.</p>
""",
        "content_en": """
<h2>The Core Idea</h2>
<p><b>Extraversion (E)</b> tends to recharge through interaction, discussion, and external stimulation. <b>Introversion (I)</b> tends to recover through quiet time, deep focus, and more controlled stimulation. This is not about liking people or being antisocial—it is about <i>how you recharge</i>.</p>

<h2>Real‑Life Examples</h2>
<p>In a long meeting, E often finds ideas flowing while talking. I can still participate actively, but may need pauses to process and craft responses. After a social event, E might feel more energized, while I may need recovery time.</p>

<h2>Practical Strategies</h2>
<ul>
  <li><b>If you’re E</b>: schedule deep‑work blocks with fewer meetings to avoid overstimulation. Use notes to keep ideas structured.</li>
  <li><b>If you’re I</b>: plan recovery time after intense collaboration. Use written communication to share ideas clearly.</li>
  <li><b>For both</b>: try a rhythm of <i>meeting → focus → review</i> to stabilize energy.</li>
</ul>

<h2>A 7‑Day Exercise</h2>
<p>For one week, track two things: (1) activities that raise your energy, (2) activities that drain it. Then adjust your calendar: add 10–20% more “recharge” time and reduce your biggest drain trigger by one step.</p>
""",
    },
    {
        "id": "a05",
        "title_id": "S vs N: Detail vs Pola",
        "title_en": "S vs N: Details vs Patterns",
        "category_id": "MBTI",
        "category_en": "MBTI",
        "read_time": "8 min",
        "summary_id": "Perbedaan menangkap informasi: konkret-detail (S) vs pola-kemungkinan (N) dan cara kolaborasi.",
        "summary_en": "Concrete details (S) vs patterns and possibilities (N), and how to collaborate.",
        "content_id": """
<h2>Perbedaan Utama</h2>
<p><b>Sensing (S)</b> cenderung fokus pada fakta, data yang terlihat, pengalaman langsung, serta langkah konkret. <b>Intuition (N)</b> cenderung fokus pada pola, koneksi ide, makna di balik data, dan kemungkinan masa depan. Keduanya sama-sama bernilai; masalah muncul ketika satu pihak menganggap gaya lainnya “kurang masuk akal” atau “kurang kreatif”.</p>

<h2>Bagaimana Ini Terlihat di Kerja</h2>
<ul>
  <li>S lebih nyaman dengan kebutuhan jelas: requirement, contoh, dan batasan.</li>
  <li>N lebih nyaman dengan ruang eksplorasi: alasan, tujuan besar, dan opsi.</li>
</ul>

<h2>Kolaborasi yang Sehat</h2>
<p>Dalam tim, S membantu N agar ide punya langkah nyata dan estimasi realistis. N membantu S melihat arah jangka panjang dan peluang inovasi. Kuncinya adalah menyepakati format komunikasi: N menyampaikan <b>mengapa</b> dan <b>gambaran besar</b>; S merinci <b>apa</b> dan <b>bagaimana</b>.</p>

<h2>Latihan Penyeimbang</h2>
<ul>
  <li>Jika Anda S: 1×/minggu buat mind‑map “kemungkinan” sebelum eksekusi. Tanyakan: “Apa 3 opsi lain?”</li>
  <li>Jika Anda N: setiap hari tulis 3 langkah konkret paling kecil yang bisa dilakukan hari ini.</li>
</ul>

<p>Gunakan perbedaan ini untuk memperkuat kualitas keputusan: ide besar yang bisa dieksekusi.</p>
""",
        "content_en": """
<h2>The Main Difference</h2>
<p><b>Sensing (S)</b> tends to focus on observable facts, concrete data, direct experience, and step‑by‑step execution. <b>Intuition (N)</b> tends to focus on patterns, connections, meaning behind data, and future possibilities. Both are valuable; conflict happens when one side assumes the other is “not logical enough” or “not creative enough.”</p>

<h2>How It Shows Up at Work</h2>
<ul>
  <li>S often prefers clear requirements, examples, and constraints.</li>
  <li>N often prefers exploration space, rationale, and multiple options.</li>
</ul>

<h2>Healthy Collaboration</h2>
<p>In teams, S helps N turn ideas into realistic steps and estimates. N helps S see long‑term direction and innovation opportunities. A useful communication agreement: N shares <b>why</b> and the <b>big picture</b>; S clarifies <b>what</b> and <b>how</b>.</p>

<h2>Balancing Exercises</h2>
<ul>
  <li>If you’re S: once a week, do a quick “possibility map” before execution. Ask: “What are 3 other options?”</li>
  <li>If you’re N: every day, write the 3 smallest concrete steps you can take today.</li>
</ul>

<p>Use this difference to improve decisions: big ideas that can actually ship.</p>
""",
    },
    {
        "id": "a06",
        "title_id": "T vs F: Logika vs Nilai",
        "title_en": "T vs F: Logic vs Values",
        "category_id": "MBTI",
        "category_en": "MBTI",
        "read_time": "8 min",
        "summary_id": "Bagaimana Thinking dan Feeling mengambil keputusan, plus cara mengurangi konflik komunikasi.",
        "summary_en": "How Thinking and Feeling decide, plus conflict‑reducing communication habits.",
        "content_id": """
<h2>Inti Preferensi</h2>
<p><b>Thinking (T)</b> cenderung menilai keputusan lewat logika, konsistensi, dan kriteria objektif. <b>Feeling (F)</b> cenderung menilai keputusan lewat nilai, harmoni, dan dampak pada manusia. Bukan berarti T “tidak punya empati” atau F “tidak logis”. Keduanya hanya punya titik awal yang berbeda.</p>

<h2>Konflik yang Sering Terjadi</h2>
<ul>
  <li>T menganggap F “terlalu sensitif” karena fokus pada perasaan dan relasi.</li>
  <li>F menganggap T “terlalu dingin” karena fokus pada aturan dan efisiensi.</li>
</ul>

<h2>Bridge Skill untuk Diskusi Sulit</h2>
<ul>
  <li><b>Jika Anda T</b>: mulai dengan empati singkat (“Saya paham ini penting buat kamu…”) sebelum memberi kritik. Jelaskan kriteria secara jelas agar terasa adil.</li>
  <li><b>If Anda F</b>: rangkum kriteria dan data (“Agar jelas, kita pakai 3 kriteria…”) sebelum menyimpulkan. Ajukan dampak manusia sebagai bagian dari kriteria, bukan hanya emosi.</li>
</ul>

<h2>Latihan 10 Menit</h2>
<p>Pilih satu keputusan kecil hari ini. Tulis dua kolom: (1) kriteria objektif, (2) dampak terhadap orang. Ambil keputusan yang menghormati keduanya. Ini melatih keseimbangan dan mengurangi bias preferensi.</p>
""",
        "content_en": """
<h2>The Core Preference</h2>
<p><b>Thinking (T)</b> tends to evaluate decisions using logic, consistency, and objective criteria. <b>Feeling (F)</b> tends to evaluate decisions using values, harmony, and human impact. This does not mean T lacks empathy or F lacks logic. They simply start from different default lenses.</p>

<h2>Typical Friction Points</h2>
<ul>
  <li>T may see F as “too sensitive” for emphasizing feelings and relationships.</li>
  <li>F may see T as “too cold” for emphasizing rules and efficiency.</li>
</ul>

<h2>Bridge Skills for Hard Conversations</h2>
<ul>
  <li><b>If you’re T</b>: start with brief empathy (“I understand this matters to you…”) before critique. State criteria clearly so it feels fair.</li>
  <li><b>If you’re F</b>: summarize criteria and data (“Let’s use 3 criteria…”) before concluding. Frame human impact as part of the criteria, not as “just emotion.”</li>
</ul>

<h2>A 10‑Minute Practice</h2>
<p>Pick one small decision today. Write two columns: (1) objective criteria, (2) human impact. Make a decision that respects both. This trains balance and reduces preference bias.</p>
""",
    },
    {
        "id": "a07",
        "title_id": "J vs P: Struktur vs Fleksibilitas",
        "title_en": "J vs P: Structure vs Flexibility",
        "category_id": "MBTI",
        "category_en": "MBTI",
        "read_time": "8 min",
        "summary_id": "Gaya kerja: rencana jelas (J) vs adaptif (P), dan cara menyelaraskan di tim.",
        "summary_en": "Work style: planned structure (J) vs adaptive flexibility (P), and how to align in teams.",
        "content_id": """
<h2>Preferensi Mengelola Hidup</h2>
<p><b>Judging (J)</b> cenderung nyaman dengan struktur, keputusan, dan kepastian. <b>Perceiving (P)</b> cenderung nyaman dengan fleksibilitas, eksplorasi, dan opsi terbuka. J bukan berarti kaku, P bukan berarti berantakan—keduanya adalah strategi mengelola ketidakpastian.</p>

<h2>Bagaimana Ini Terlihat</h2>
<ul>
  <li>J suka rencana jelas, checklist, dan merasa tenang ketika keputusan sudah dibuat.</li>
  <li>P suka ruang adaptasi, belajar sambil jalan, dan merasa tercekik oleh rencana terlalu detail.</li>
</ul>

<h2>Kesepakatan Tim yang Menyelamatkan</h2>
<p>Jika Anda bekerja lintas gaya, buat “kontrak kerja” sederhana: <b>deadline keras</b>, <b>zona eksplorasi</b>, dan <b>definisi done</b>. P dapat mengeksplorasi dalam zona itu, sementara J punya kepastian kapan hasil harus final.</p>

<h2>Latihan Penyeimbang</h2>
<ul>
  <li>Jika Anda J: sisakan buffer untuk perubahan. Latih fleksibilitas dengan satu eksperimen kecil per minggu.</li>
  <li>Jika Anda P: pakai “minimal plan”: 3 milestone + 1 review rutin. Ini memberi arah tanpa membuat Anda kehilangan ruang adaptasi.</li>
</ul>
""",
        "content_en": """
<h2>Preferences for Managing Life</h2>
<p><b>Judging (J)</b> tends to prefer structure, decisions, and closure. <b>Perceiving (P)</b> tends to prefer flexibility, exploration, and keeping options open. J is not automatically rigid, and P is not automatically messy—both are ways of managing uncertainty.</p>

<h2>How It Shows Up</h2>
<ul>
  <li>J often likes clear plans, checklists, and feels calm after decisions are made.</li>
  <li>P often likes adaptive space, learns by doing, and feels constrained by overly detailed plans.</li>
</ul>

<h2>A Team Agreement That Saves Projects</h2>
<p>When you collaborate across styles, create a simple “working contract”: a <b>hard deadline</b>, an <b>exploration zone</b>, and a <b>definition of done</b>. P can explore within the zone, while J gets clarity on when the output must be finalized.</p>

<h2>Balancing Exercises</h2>
<ul>
  <li>If you’re J: leave buffer for change. Practice flexibility through one small experiment each week.</li>
  <li>If you’re P: use a “minimal plan”: 3 milestones + one regular review. It adds direction without removing adaptability.</li>
</ul>
""",
    },

    # --- Big Five ---
    {
        "id": "a08",
        "title_id": "Big Five: Kenapa OCEAN Paling Banyak Dipakai Riset",
        "title_en": "Big Five: Why OCEAN Is Widely Used in Research",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "8 min",
        "summary_id": "Big Five populer karena stabil, terukur, dan banyak dipakai dalam riset psikologi modern.",
        "summary_en": "Big Five is popular because it is measurable, stable, and widely used in modern research.",
        "content_id": """
<h2>Kenapa Big Five?</h2>
<p>Big Five (OCEAN) adalah model trait yang sangat umum dipakai dalam riset karena sifatnya <b>dimensional</b>: Anda punya tingkat pada setiap dimensi, bukan sekadar masuk kotak kategori. Model ini juga relatif stabil lintas waktu dan lintas budaya ketika diukur dengan alat yang baik.</p>

<h2>5 Dimensi</h2>
<ul>
  <li><b>O</b> (Openness/Keterbukaan): rasa ingin tahu, imajinasi, fleksibilitas ide.</li>
  <li><b>C</b> (Conscientiousness/Ketekunan): disiplin, keteraturan, kontrol diri.</li>
  <li><b>E</b> (Extraversion/Ekstroversi): energi sosial, asertivitas, stimulasi.</li>
  <li><b>A</b> (Agreeableness/Keramahan): empati, kooperatif, kepercayaan.</li>
  <li><b>N</b> (Neuroticism/Neurotisisme): sensitivitas stres, reaktivitas emosi.</li>
</ul>

<h2>Cara Membaca Hasil</h2>
<p>Lihat pola kombinasi. Misalnya, C tinggi + N tinggi dapat berarti sangat teliti tetapi mudah khawatir; Anda butuh sistem kerja yang rapi plus strategi regulasi stres. O tinggi + E tinggi dapat berarti ide melimpah dan nyaman berdiskusi; Anda butuh teknik prioritas agar tidak “menyebar”.</p>

<p>Gunakan OCEAN untuk merancang kebiasaan: apa yang perlu diperkuat, apa yang perlu diseimbangkan, dan lingkungan seperti apa yang membuat Anda bertumbuh.</p>
""",
        "content_en": """
<h2>Why Big Five?</h2>
<p>Big Five (OCEAN) is widely used in research because it is <b>dimensional</b>: you have a level on each trait rather than being forced into a single category box. With well‑designed measures, the model is also relatively stable across time and across cultures.</p>

<h2>The Five Traits</h2>
<ul>
  <li><b>O</b> (Openness): curiosity, imagination, cognitive flexibility.</li>
  <li><b>C</b> (Conscientiousness): discipline, organization, self‑control.</li>
  <li><b>E</b> (Extraversion): social energy, assertiveness, stimulation.</li>
  <li><b>A</b> (Agreeableness): empathy, cooperation, trust.</li>
  <li><b>N</b> (Neuroticism): stress sensitivity, emotional reactivity.</li>
</ul>

<h2>How to Read Results</h2>
<p>Look at combinations. For example, high C + high N may mean you are careful and thorough but prone to worry; you benefit from clear systems and stress‑regulation habits. High O + high E may mean lots of ideas and comfort with discussion; you may need prioritization to avoid spreading yourself too thin.</p>

<p>Use OCEAN to design habits: what to strengthen, what to balance, and which environments help you grow.</p>
""",
    },

    # Articles a09..a25 are provided in a separate section below to keep this file readable.
]


# Append the remaining articles (a09..a25)
ARTICLES += [
    {
        "id": "a09",
        "title_id": "Openness: Kreativitas, Rasa Ingin Tahu, dan Adaptasi",
        "title_en": "Openness: Curiosity, Creativity, and Adaptation",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "8 min",
        "summary_id": "Openness tinggi sering terkait eksplorasi ide; rendah cenderung praktis dan stabil.",
        "summary_en": "High openness relates to exploration; low openness tends to be practical and steady.",
        "content_id": """
<h2>Makna Openness</h2>
<p>Openness menggambarkan kecenderungan untuk tertarik pada ide baru, pengalaman baru, dan cara pandang yang beragam. Skor tinggi sering terkait rasa ingin tahu, imajinasi, dan kenyamanan pada perubahan. Skor rendah biasanya terkait preferensi pada hal yang familiar, praktis, dan stabil.</p>

<h2>Kekuatan dan Risiko</h2>
<ul>
  <li><b>O tinggi</b>: mudah melihat alternatif, cepat belajar lintas bidang, cocok untuk inovasi. Risiko: terlalu banyak ide, sulit memilih prioritas.</li>
  <li><b>O rendah</b>: fokus eksekusi, realistis, kuat dalam menjaga standar yang sudah terbukti. Risiko: menolak perubahan terlalu cepat atau kurang eksplorasi.</li>
</ul>

<h2>Strategi Pengembangan (Actionable)</h2>
<ol>
  <li>Jika O tinggi: gunakan aturan <b>1 ide → 1 eksperimen kecil</b>. Batasi eksperimen agar tetap bisa selesai.</li>
  <li>Jika O rendah: lakukan <b>eksperimen aman</b> 15 menit: baca ringkasan buku, tonton kuliah singkat, atau coba metode kerja baru selama 1 hari.</li>
  <li>Untuk semua: buat “bank ide” lalu pilih 1 yang paling berdampak minggu ini.</li>
</ol>

<h2>Pertanyaan Refleksi</h2>
<p>Apa 1 perubahan kecil yang sebenarnya Anda inginkan, tetapi Anda tunda karena merasa tidak nyaman? Tuliskan versi “mini” yang bisa Anda coba dalam 30 menit.</p>
""",
        "content_en": """
<h2>What Openness Means</h2>
<p>Openness reflects a tendency to be interested in new ideas, new experiences, and diverse perspectives. High scores often relate to curiosity, imagination, and comfort with change. Lower scores often relate to preference for familiarity, practicality, and stability.</p>

<h2>Strengths and Risks</h2>
<ul>
  <li><b>High O</b>: sees alternatives easily, learns across domains, supports innovation. Risk: too many ideas, weak prioritization.</li>
  <li><b>Low O</b>: strong execution, realism, keeps proven standards. Risk: rejecting change too quickly or under‑exploring options.</li>
</ul>

<h2>Actionable Development</h2>
<ol>
  <li>If high O: use the rule <b>1 idea → 1 small experiment</b>. Limit experiments so you finish.</li>
  <li>If low O: run a <b>safe experiment</b> for 15 minutes—read a short summary, watch a mini‑lecture, or try a new workflow for one day.</li>
  <li>For everyone: keep an “idea bank,” then pick the single highest‑impact idea this week.</li>
</ol>

<h2>Reflection Prompt</h2>
<p>What is one small change you actually want, but you delay because it feels uncomfortable? Write a “mini version” you can test in 30 minutes.</p>
""",
    },

    {
        "id": "a10",
        "title_id": "Conscientiousness: Disiplin Tanpa Perfeksionisme",
        "title_en": "Conscientiousness: Discipline Without Perfectionism",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "8 min",
        "summary_id": "C tinggi membantu konsistensi; tantangannya adalah overcontrol dan perfeksionisme.",
        "summary_en": "High C supports consistency; the challenge is overcontrol and perfectionism.",
        "content_id": """
<h2>Apa itu Conscientiousness?</h2>
<p>Conscientiousness (C) berkaitan dengan disiplin, keteraturan, dan kemampuan menunda kepuasan untuk hasil jangka panjang. Ini bukan sekadar “rajin”, tetapi juga cara Anda mengelola komitmen: apakah Anda konsisten, rapi, dan mudah menyelesaikan sesuatu sampai tuntas.</p>

<h2>Kekuatan dan Tantangan</h2>
<ul>
  <li><b>C tinggi</b>: dapat diandalkan, rapi, kuat dalam perencanaan. Tantangan: perfeksionisme, sulit delegasi, mudah frustrasi ketika standar tidak terpenuhi.</li>
  <li><b>C rendah</b>: fleksibel, cepat beradaptasi, tidak mudah terjebak aturan. Tantangan: kurang konsisten, mudah menunda, detail terlewat.</li>
</ul>

<h2>Strategi Profesional</h2>
<ol>
  <li><b>Definisi “done”</b>: tulis kriteria selesai 3–5 poin (bukan 20) agar fokus.</li>
  <li><b>Time‑boxing</b>: beri batas waktu untuk kualitas “cukup baik” sebelum revisi.</li>
  <li><b>Delegasi cerdas</b>: delegasikan <i>output</i> + <i>standar minimum</i> + <i>check‑in</i>, bukan delegasi “tebakan”.</li>
  <li><b>Sistem 2 daftar</b>: (1) prioritas hari ini, (2) backlog. Ini menurunkan rasa kewalahan.</li>
</ol>

<h2>Latihan 7 Hari</h2>
<p>Pilih satu kebiasaan: “3 prioritas harian” atau “review 10 menit sore”. Catat 1 hal yang berhasil dan 1 hal yang mengganggu konsistensi. Tujuannya bukan sempurna, tetapi stabil.</p>
""",
        "content_en": """
<h2>What Is Conscientiousness?</h2>
<p>Conscientiousness (C) relates to discipline, organization, and the ability to delay gratification for long‑term outcomes. It is not just “being hardworking.” It is how you manage commitments: whether you are consistent, structured, and able to finish what you start.</p>

<h2>Strengths and Challenges</h2>
<ul>
  <li><b>High C</b>: reliable, organized, strong planner. Challenge: perfectionism, difficulty delegating, frustration when standards are not met.</li>
  <li><b>Low C</b>: flexible, adaptive, not overly constrained by rules. Challenge: inconsistency, procrastination, missing details.</li>
</ul>

<h2>Professional Strategies</h2>
<ol>
  <li><b>Definition of done</b>: write 3–5 completion criteria (not 20) to stay focused.</li>
  <li><b>Time‑boxing</b>: set a time limit for “good enough” before additional polishing.</li>
  <li><b>Smart delegation</b>: delegate the <i>output</i> + <i>minimum standard</i> + <i>check‑in cadence</i>, not guesswork.</li>
  <li><b>Two‑list system</b>: (1) today’s priorities, (2) backlog. This reduces overwhelm.</li>
</ol>

<h2>7‑Day Practice</h2>
<p>Pick one habit: “3 daily priorities” or a “10‑minute evening review.” Track one thing that worked and one friction point each day. The goal is stability, not perfection.</p>
""",
    },

    {
        "id": "a11",
        "title_id": "Extraversion: Energi, Asertif, dan Stimulus",
        "title_en": "Extraversion: Energy, Assertiveness, and Stimulation",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "8 min",
        "summary_id": "E tinggi bukan berarti selalu suka ramai; ini tentang kebutuhan stimulasi dan ekspresi.",
        "summary_en": "High E isn't just being social; it's about stimulation needs and outward expression.",
        "content_id": """
<h2>Makna Extraversion</h2>
<p>Dalam Big Five, Extraversion (E) berkaitan dengan energi sosial, asertivitas, dan kebutuhan stimulasi. Skor tinggi sering tampak sebagai ekspresif, proaktif, dan nyaman mengambil ruang bicara. Skor rendah sering tampak sebagai tenang, fokus, dan lebih memilih interaksi yang dalam daripada banyak interaksi.</p>

<h2>Kesalahpahaman Umum</h2>
<p>E rendah bukan berarti “anti sosial”, dan E tinggi bukan berarti “selalu suka keramaian”. Banyak orang E tinggi tetap butuh waktu sendiri untuk recovery. Yang berbeda adalah seberapa mudah Anda mengaktifkan energi lewat stimulus luar dan seberapa nyaman Anda mengekspresikan diri.</p>

<h2>Strategi Kerja</h2>
<ul>
  <li><b>E tinggi</b>: buat blok fokus tanpa gangguan agar ide tidak menguap di meeting. Batasi rapat back‑to‑back.</li>
  <li><b>E rendah</b>: gunakan komunikasi tertulis untuk memperjelas ide, lalu pilih momen bicara yang berdampak tinggi.</li>
  <li><b>Tim campuran</b>: gunakan agenda 3 poin, outcome jelas, dan sesi tanya‑jawab singkat.</li>
</ul>

<h2>Latihan</h2>
<p>Selama 5 hari, catat: interaksi apa yang memberi energi dan apa yang menguras. Dari catatan itu, desain rutinitas: 1 slot sosial + 1 slot fokus setiap hari kerja.</p>
""",
        "content_en": """
<h2>What Extraversion Means</h2>
<p>In the Big Five, Extraversion (E) relates to social energy, assertiveness, and stimulation needs. Higher E often looks like expressive, proactive, and comfortable taking the floor. Lower E often looks like calm, focused, and preferring fewer but deeper interactions.</p>

<h2>A Common Misunderstanding</h2>
<p>Low E is not “anti‑social,” and high E is not “always loves crowds.” Many high‑E people still need quiet recovery time. The difference is how easily external stimulation activates your energy and how comfortable you are expressing yourself outwardly.</p>

<h2>Work Strategies</h2>
<ul>
  <li><b>High E</b>: protect deep‑focus blocks so your ideas do not evaporate into meetings. Avoid back‑to‑back calls.</li>
  <li><b>Low E</b>: use writing to clarify thinking, then choose high‑impact moments to speak up.</li>
  <li><b>Mixed teams</b>: keep a 3‑point agenda, define outcomes, and allow a short Q&amp;A window.</li>
</ul>

<h2>Practice</h2>
<p>For five days, track which interactions energize you and which drain you. Then design a routine: one social slot + one focus slot each workday.</p>
""",
    },

    {
        "id": "a12",
        "title_id": "Agreeableness: Empati, Kerjasama, dan Boundaries",
        "title_en": "Agreeableness: Empathy, Cooperation, and Boundaries",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "8 min",
        "summary_id": "A tinggi mendukung harmoni; tetap butuh batas agar tidak mudah dimanfaatkan.",
        "summary_en": "High A supports harmony; boundaries prevent over‑accommodation.",
        "content_id": """
<h2>Makna Agreeableness</h2>
<p>Agreeableness (A) berkaitan dengan empati, kooperatif, dan kecenderungan mempercayai orang lain. A tinggi biasanya hangat dan mudah bekerja sama. A rendah biasanya lebih kritis, langsung, dan kuat dalam debat prinsip.</p>

<h2>Kekuatan dan Risiko</h2>
<ul>
  <li><b>A tinggi</b>: membangun kepercayaan cepat, menenangkan konflik, menjaga relasi. Risiko: people‑pleasing, sulit menolak, menumpuk beban.</li>
  <li><b>A rendah</b>: jujur, tegas, mampu menantang ide buruk. Risiko: terdengar keras, memicu defensif jika tidak disertai empati.</li>
</ul>

<h2>Boundaries yang Profesional</h2>
<p>Boundaries bukan berarti kasar; boundaries berarti jelas. Gunakan kalimat “<b>yes, if…</b>”: “Saya bisa bantu, <i>jika</i> prioritas A selesai dulu” atau “Saya bisa ambil ini, <i>jika</i> deadline mundur ke Jumat.” Ini menjaga kualitas kerja tanpa merusak relasi.</p>

<h2>Latihan Komunikasi</h2>
<ol>
  <li>Tulis 2 kalimat penolakan yang tetap sopan.</li>
  <li>Latih “kritik + alasan + alternatif” agar diskusi tetap aman.</li>
  <li>Setiap minggu, evaluasi: kapan saya berkata “iya” padahal seharusnya “tidak”?</li>
</ol>
""",
        "content_en": """
<h2>What Agreeableness Means</h2>
<p>Agreeableness (A) relates to empathy, cooperativeness, and a tendency to trust others. High A is often warm and collaborative. Low A is often more critical, direct, and comfortable challenging ideas.</p>

<h2>Strengths and Risks</h2>
<ul>
  <li><b>High A</b>: builds trust quickly, de‑escalates conflict, maintains relationships. Risk: people‑pleasing, difficulty saying no, overload.</li>
  <li><b>Low A</b>: honest, firm, good at challenging bad ideas. Risk: sounding harsh or triggering defensiveness without empathy.</li>
</ul>

<h2>Professional Boundaries</h2>
<p>Boundaries are not rudeness; they are clarity. Use “<b>yes, if…</b>”: “I can help <i>if</i> priority A is finished first,” or “I can take this <i>if</i> the deadline moves to Friday.” This protects quality without damaging relationships.</p>

<h2>Communication Practice</h2>
<ol>
  <li>Write two polite refusal sentences you can reuse.</li>
  <li>Practice “critique + reason + alternative” to keep discussions safe.</li>
  <li>Weekly review: when did I say yes when I should have said no?</li>
</ol>
""",
    },

    {
        "id": "a13",
        "title_id": "Neuroticism: Stres, Emosi, dan Regulasi Diri",
        "title_en": "Neuroticism: Stress, Emotion, and Self‑Regulation",
        "category_id": "Big Five",
        "category_en": "Big Five",
        "read_time": "9 min",
        "summary_id": "N tinggi berarti lebih sensitif terhadap stres; kabar baiknya, regulasi diri bisa dilatih.",
        "summary_en": "High N means higher stress sensitivity; self‑regulation skills can be trained.",
        "content_id": """
<h2>Makna Neuroticism</h2>
<p>Neuroticism (N) menggambarkan seberapa sensitif Anda terhadap stres dan seberapa kuat reaksi emosi negatif (cemas, tegang, mudah tersinggung). N tinggi tidak berarti “lemah”; sering kali itu berarti sistem Anda cepat mendeteksi risiko. Tantangannya adalah mengelola reaksi agar tidak melebar menjadi overthinking.</p>

<h2>Tanda yang Sering Muncul</h2>
<ul>
  <li>Over‑analysis sebelum memulai pekerjaan.</li>
  <li>Sulit “mematikan pikiran” saat malam.</li>
  <li>Mudah merasa bersalah atau khawatir tanpa bukti kuat.</li>
</ul>

<h2>Strategi Regulasi (3 Level)</h2>
<ol>
  <li><b>Fisiologis</b>: napas 4‑6 (tarik 4 detik, hembus 6 detik) selama 2 menit.</li>
  <li><b>Kognitif</b>: tulis “fakta vs asumsi”. Pisahkan data nyata dari pikiran otomatis.</li>
  <li><b>Perilaku</b>: ambil tindakan kecil dalam 10 menit. Aksi kecil menurunkan rasa tidak berdaya.</li>
</ol>

<h2>Latihan 1 Minggu</h2>
<p>Setiap kali cemas muncul, beri label: “Saya merasa … karena …” lalu pilih 1 aksi kecil (mengirim pesan, membuat outline, meminta klarifikasi). Tujuannya membangun kebiasaan <i>regulate → act</i>.</p>
""",
        "content_en": """
<h2>What Neuroticism Means</h2>
<p>Neuroticism (N) reflects how sensitive you are to stress and how strongly you react with negative emotions (anxiety, tension, irritability). High N does not mean “weak.” It often means your system detects risk quickly. The challenge is managing reactions so they do not expand into rumination.</p>

<h2>Common Signs</h2>
<ul>
  <li>Over‑analyzing before starting tasks.</li>
  <li>Difficulty “switching off” at night.</li>
  <li>Feeling guilty or worried without strong evidence.</li>
</ul>

<h2>Regulation Strategies (3 Levels)</h2>
<ol>
  <li><b>Physiological</b>: 4‑6 breathing (inhale 4 seconds, exhale 6) for 2 minutes.</li>
  <li><b>Cognitive</b>: write “facts vs assumptions.” Separate real data from automatic thoughts.</li>
  <li><b>Behavioral</b>: take a small action within 10 minutes. Action reduces helplessness.</li>
</ol>

<h2>One‑Week Practice</h2>
<p>Whenever anxiety appears, label it: “I feel … because …” then choose one small action (send a message, create an outline, ask for clarification). The goal is a <i>regulate → act</i> habit.</p>
""",
    },

    {
        "id": "a14",
        "title_id": "Enneagram: Motivasi Inti dan Pola Pertahanan",
        "title_en": "Enneagram: Core Motivations and Defense Patterns",
        "category_id": "Enneagram",
        "category_en": "Enneagram",
        "read_time": "9 min",
        "summary_id": "Enneagram fokus pada motivasi inti (apa yang Anda kejar/hindari) dan pola coping.",
        "summary_en": "Enneagram focuses on core motivations (what you seek/avoid) and coping patterns.",
        "content_id": """
<h2>Fokus Enneagram</h2>
<p>Enneagram sering menarik karena menyorot <b>motivasi inti</b>: kebutuhan, ketakutan, dan pola pertahanan yang muncul otomatis saat tertekan. Dua orang bisa berperilaku mirip, tetapi motivasinya berbeda. Misalnya, sama‑sama perfeksionis: satu karena ingin “benar”, satu karena takut dinilai gagal.</p>

<h2>Manfaat Praktis</h2>
<ul>
  <li>Memahami pola stres: apa respons otomatis Anda ketika terancam?</li>
  <li>Melatih pilihan sadar: mengganti reaksi otomatis dengan respons yang lebih sehat.</li>
  <li>Membangun empati: melihat bahwa orang lain juga digerakkan oleh kebutuhan tertentu.</li>
</ul>

<h2>Cara Memakai Secara Aman</h2>
<ol>
  <li>Gunakan hasil sebagai hipotesis: “mungkin saya cenderung …”.</li>
  <li>Validasi dengan contoh: kapan pola itu muncul, dan apa dampaknya?</li>
  <li>Pilih 1 kebiasaan penyeimbang selama 14 hari (bukan 10 kebiasaan sekaligus).</li>
</ol>

<h2>Mini‑Exercise</h2>
<p>Tulis 3 situasi terakhir yang membuat Anda defensif. Untuk tiap situasi, jawab: (1) apa yang saya takutkan, (2) apa yang sebenarnya saya butuhkan, (3) cara sehat meminta kebutuhan itu.</p>
""",
        "content_en": """
<h2>The Enneagram Focus</h2>
<p>The Enneagram is compelling because it highlights <b>core motivations</b>: needs, fears, and defense patterns that show up automatically under stress. Two people can behave similarly but be driven by different motives. For example, both may appear perfectionistic—one because they want to be “right,” another because they fear being seen as a failure.</p>

<h2>Practical Benefits</h2>
<ul>
  <li>Understand stress patterns: what is your automatic reaction when you feel threatened?</li>
  <li>Build conscious choice: replace reflexive reactions with healthier responses.</li>
  <li>Increase empathy: see that others are also driven by needs.</li>
</ul>

<h2>How to Use It Safely</h2>
<ol>
  <li>Treat results as a hypothesis: “I might tend to …”.</li>
  <li>Validate with examples: when does it show up, and what is the impact?</li>
  <li>Choose one balancing habit for 14 days (not ten at once).</li>
</ol>

<h2>Mini Exercise</h2>
<p>Write three recent situations that made you defensive. For each, answer: (1) what did I fear, (2) what did I truly need, (3) how can I request that need in a healthy way?</p>
""",
    },

    {
        "id": "a15",
        "title_id": "Enneagram: Wings & Jalur Growth/Stres",
        "title_en": "Enneagram: Wings and Growth/Stress Lines",
        "category_id": "Enneagram",
        "category_en": "Enneagram",
        "read_time": "9 min",
        "summary_id": "Memahami wing dan arah growth/stres agar refleksi lebih tajam dan tidak kaku.",
        "summary_en": "Understand wings and growth/stress lines to make reflection sharper and less rigid.",
        "content_id": """
<h2>Wing: “Warna Tambahan”</h2>
<p>Wing adalah tipe di sebelah tipe utama yang memberi pengaruh tambahan. Misalnya, Tipe 1 bisa memiliki nuansa 1w9 (lebih tenang) atau 1w2 (lebih membantu). Wing bukan berarti Anda punya dua tipe; wing adalah variasi gaya di dalam tipe Anda.</p>

<h2>Growth dan Stress</h2>
<p>Banyak literatur Enneagram menggambarkan bahwa saat berkembang, Anda mengadopsi kualitas sehat tertentu; saat stres, pola tertentu menguat. Cara paling aman memakainya adalah sebagai bahasa untuk mengamati diri, bukan ramalan mutlak.</p>

<h2>Tips Penggunaan</h2>
<ul>
  <li>Amati kondisi: saya sedang <b>stabil</b>, <b>stres</b>, atau <b>berkembang</b>?</li>
  <li>Catat pemicu: situasi, kata, atau peristiwa apa yang memicu reaksi?</li>
  <li>Rancang respons: 1 perilaku kecil yang meniru “versi sehat” Anda.</li>
</ul>

<h2>Latihan 14 Hari</h2>
<p>Pilih satu kualitas growth yang ingin dilatih. Contoh: lebih tenang, lebih berani, atau lebih terstruktur. Setiap hari, lakukan 1 aksi kecil yang konsisten, lalu refleksikan: apakah saya merasa lebih efektif dan lebih damai?</p>
""",
        "content_en": """
<h2>Wings: Extra Flavor</h2>
<p>A wing is an adjacent type that adds flavor to your core type. For instance, Type 1 may look like 1w9 (calmer) or 1w2 (more helper‑oriented). A wing does not mean you have two types; it is a variation within your type.</p>

<h2>Growth and Stress Lines</h2>
<p>Many Enneagram traditions describe that under growth you adopt healthier qualities, and under stress certain patterns intensify. The safest way to use this is as a language for self‑observation—not a rigid prediction.</p>

<h2>Practical Tips</h2>
<ul>
  <li>Check your state: am I <b>stable</b>, <b>stressed</b>, or <b>growing</b>?</li>
  <li>Track triggers: which situations, words, or events activate reactions?</li>
  <li>Design a response: one small behavior that matches your “healthy version.”</li>
</ul>

<h2>14‑Day Practice</h2>
<p>Pick one growth quality to train—calmness, courage, structure, etc. Each day, do one consistent small action, then reflect: do I feel more effective and more at peace?</p>
""",
    },

    {
        "id": "a16",
        "title_id": "4 Temperaments: Cara Membaca & Menggunakannya",
        "title_en": "Four Temperaments: How to Read and Use Them",
        "category_id": "Temperament",
        "category_en": "Temperament",
        "read_time": "8 min",
        "summary_id": "Temperament menggambarkan gaya energi dan interaksi yang mudah dikenali dalam keseharian.",
        "summary_en": "Temperaments describe energy and interaction styles that are easy to observe in daily life.",
        "content_id": """
<h2>Gambaran 4 Temperament</h2>
<p>Model temperament klasik sering digunakan sebagai bahasa sederhana untuk gaya energi dan interaksi. Ini bukan model ilmiah modern seperti Big Five, tetapi bisa membantu refleksi awal—selama dipakai dengan bijak dan tidak kaku.</p>

<ul>
  <li><b>Sanguine</b>: ekspresif, spontan, mudah membangun koneksi.</li>
  <li><b>Choleric</b>: tegas, cepat, berorientasi hasil.</li>
  <li><b>Phlegmatic</b>: tenang, stabil, pendamai.</li>
  <li><b>Melancholic</b>: teliti, analitis, detail.</li>
</ul>

<h2>Kolaborasi</h2>
<p>Konflik sering bukan karena niat buruk, tetapi karena gaya berbeda. Choleric bisa terlihat “terburu‑buru” bagi Melancholic; Melancholic bisa terlihat “lama” bagi Choleric. Solusinya adalah menyepakati ritme: kapan eksplorasi detail dibutuhkan, kapan keputusan harus dibuat.</p>

<h2>Latihan</h2>
<p>Identifikasi gaya dominan Anda, lalu latih kebiasaan penyeimbang. Contoh: jika Anda Choleric, latih 1 pertanyaan empatik sebelum memberi arahan. Jika Anda Melancholic, latih 1 keputusan cepat per hari dengan data minimum yang cukup.</p>
""",
        "content_en": """
<h2>The Four Temperaments</h2>
<p>The classic temperament model is often used as a simple language for energy and interaction style. It is not as evidence‑based as modern trait models like Big Five, but it can support early self‑reflection—if you avoid rigid labeling.</p>

<ul>
  <li><b>Sanguine</b>: expressive, spontaneous, connects easily.</li>
  <li><b>Choleric</b>: decisive, fast, results‑oriented.</li>
  <li><b>Phlegmatic</b>: calm, steady, peace‑oriented.</li>
  <li><b>Melancholic</b>: detailed, analytical, precision‑oriented.</li>
</ul>

<h2>Collaboration</h2>
<p>Conflict often comes from style differences, not bad intent. Choleric may look “too rushed” to Melancholic; Melancholic may look “too slow” to Choleric. The fix is agreeing on rhythm: when detail exploration is needed, and when decisions must be made.</p>

<h2>Practice</h2>
<p>Identify your dominant style and practice a balancing habit. If you are Choleric, ask one empathy question before giving direction. If you are Melancholic, make one quick daily decision with “minimum sufficient data.”</p>
""",
    },

    {
        "id": "a17",
        "title_id": "Teknik 1% Improvement: Kebiasaan Kecil, Dampak Besar",
        "title_en": "The 1% Improvement Method: Small Habits, Big Results",
        "category_id": "Self-Development",
        "category_en": "Self‑Development",
        "read_time": "8 min",
        "summary_id": "Cara membangun rutinitas pengembangan diri tanpa merasa berat dan tanpa perfeksionisme.",
        "summary_en": "Build self‑development routines without perfectionism or overwhelm.",
        "content_id": """
<h2>Kenapa 1%?</h2>
<p>Perubahan besar sering gagal karena terlalu berat dan sulit diulang. Prinsip 1% mengatakan: pilih perubahan kecil yang cukup mudah dilakukan, lalu ulangi sampai menjadi identitas. Dalam jangka panjang, konsistensi mengalahkan intensitas.</p>

<h2>Rumus Sederhana</h2>
<ul>
  <li><b>Trigger</b>: setelah kegiatan tertentu (misalnya setelah mandi).</li>
  <li><b>Action</b>: kebiasaan kecil (misalnya tulis 3 prioritas).</li>
  <li><b>Reward</b>: tanda selesai (centang checklist, minum teh, dll).</li>
</ul>

<h2>Contoh yang Relevan dengan Kepribadian</h2>
<p>Jika Anda mudah overthinking (N tinggi), kebiasaan 1% bisa berupa “napas 2 menit” sebelum membuka email. Jika Anda ide banyak (O tinggi), kebiasaan 1% bisa berupa “pilih 1 ide untuk dieksekusi hari ini”.</p>

<h2>Latihan 7 Hari</h2>
<ol>
  <li>Pilih 1 kebiasaan <b>maksimal 3 menit</b>.</li>
  <li>Jadwalkan di waktu tetap.</li>
  <li>Jika gagal, turunkan level (bukan berhenti).</li>
</ol>
""",
        "content_en": """
<h2>Why 1%?</h2>
<p>Big changes often fail because they are heavy and hard to repeat. The 1% principle says: choose a tiny improvement that is easy enough to do, then repeat until it becomes identity. Over time, consistency beats intensity.</p>

<h2>A Simple Formula</h2>
<ul>
  <li><b>Trigger</b>: after a specific event (e.g., after shower).</li>
  <li><b>Action</b>: a small habit (e.g., write 3 priorities).</li>
  <li><b>Reward</b>: completion signal (checklist tick, tea break, etc.).</li>
</ul>

<h2>Examples Linked to Personality</h2>
<p>If you overthink (high N), your 1% habit could be “2‑minute breathing” before opening email. If you have many ideas (high O), your 1% habit could be “pick one idea to execute today.”</p>

<h2>7‑Day Practice</h2>
<ol>
  <li>Choose one habit that takes <b>3 minutes or less</b>.</li>
  <li>Anchor it to a fixed time.</li>
  <li>If you fail, lower the bar (do not quit).</li>
</ol>
""",
    },

    {
        "id": "a18",
        "title_id": "Komunikasi Asertif: Jelas Tanpa Menyakiti",
        "title_en": "Assertive Communication: Clear Without Harm",
        "category_id": "Komunikasi",
        "category_en": "Communication",
        "read_time": "9 min",
        "summary_id": "Asertif = jelas + hormat. Bukan agresif, bukan pasif.",
        "summary_en": "Assertive means clear + respectful—not aggressive, not passive.",
        "content_id": """
<h2>Apa itu Asertif?</h2>
<p>Asertif adalah kemampuan menyampaikan kebutuhan, batas, dan pendapat secara jelas sekaligus tetap menghormati orang lain. Berbeda dengan agresif (menang sendiri) dan pasif (mengorbankan diri), asertif berusaha adil bagi kedua pihak.</p>

<h2>Template Kalimat</h2>
<ul>
  <li>“Saya merasa … ketika … karena …”</li>
  <li>“Yang saya butuhkan adalah …”</li>
  <li>“Saya bisa bantu, tapi batas saya …”</li>
</ul>

<h2>Kenapa Ini Penting untuk Berbagai Tipe</h2>
<p>Jika Anda cenderung A tinggi (mudah mengalah), asertif melindungi energi Anda. Jika Anda cenderung T tinggi (langsung), asertif membantu menyampaikan ide tanpa memicu defensif. Asertif adalah skill universal yang membuat kerja tim lebih sehat.</p>

<h2>Latihan 7 Hari</h2>
<ol>
  <li>Mulai dari situasi kecil (misalnya meminta klarifikasi).</li>
  <li>Gunakan satu template, ulangi sampai natural.</li>
  <li>Refleksi: apa reaksi orang lain? Apakah komunikasi Anda lebih efektif?</li>
</ol>
""",
        "content_en": """
<h2>What Is Assertiveness?</h2>
<p>Assertiveness is the ability to express needs, boundaries, and opinions clearly while still respecting others. Unlike aggression (winning at all costs) and passivity (self‑sacrifice), assertiveness aims for fairness for both sides.</p>

<h2>Useful Sentence Templates</h2>
<ul>
  <li>“I feel … when … because …”</li>
  <li>“What I need is …”</li>
  <li>“I can help, but my limit is …”</li>
</ul>

<h2>Why It Matters Across Types</h2>
<p>If you are high in agreeableness (you accommodate easily), assertiveness protects your energy. If you are more direct (high T‑style), assertiveness helps you deliver ideas without triggering defensiveness. It is a universal skill for healthier teamwork.</p>

<h2>7‑Day Practice</h2>
<ol>
  <li>Start with small situations (e.g., asking for clarification).</li>
  <li>Use one template repeatedly until it feels natural.</li>
  <li>Reflect: how did people respond? Did communication become more effective?</li>
</ol>
""",
    },

    {
        "id": "a19",
        "title_id": "Active Listening: Mendengar untuk Mengerti",
        "title_en": "Active Listening: Listening to Understand",
        "category_id": "Komunikasi",
        "category_en": "Communication",
        "read_time": "8 min",
        "summary_id": "Teknik mendengar aktif untuk mengurangi salah paham dan meningkatkan kepercayaan.",
        "summary_en": "Active listening reduces misunderstanding and builds trust.",
        "content_id": """
<h2>Kenapa Active Listening Penting?</h2>
<p>Banyak konflik terjadi bukan karena orang tidak peduli, tetapi karena mereka mendengar untuk membalas, bukan untuk memahami. Active listening mengubah percakapan menjadi kolaborasi: Anda menunjukkan bahwa pesan lawan bicara ditangkap dengan akurat.</p>

<h2>3 Komponen</h2>
<ul>
  <li><b>Paraphrase</b>: ulangi inti pesan dengan kata Anda.</li>
  <li><b>Clarify</b>: tanya bagian yang ambigu dengan pertanyaan spesifik.</li>
  <li><b>Validate</b>: akui emosi/niat (“Saya paham ini penting”).</li>
</ul>

<h2>Contoh Kalimat</h2>
<ul>
  <li>“Kalau saya tangkap, maksudnya … benar?”</li>
  <li>“Bagian yang paling mengganggu buat kamu adalah …?”</li>
  <li>“Apa yang kamu butuhkan dari saya sekarang?”</li>
</ul>

<h2>Latihan</h2>
<p>Dalam 3 percakapan minggu ini, lakukan aturan 2‑1‑1: 2 kali paraphrase, 1 kali clarify, 1 kali validate. Anda akan kaget betapa cepat tensi turun dan solusi muncul.</p>
""",
        "content_en": """
<h2>Why Active Listening Matters</h2>
<p>Many conflicts happen not because people do not care, but because they listen to reply—not to understand. Active listening turns a conversation into collaboration: you prove that the other person’s message was accurately received.</p>

<h2>The 3 Components</h2>
<ul>
  <li><b>Paraphrase</b>: restate the core message in your own words.</li>
  <li><b>Clarify</b>: ask specific questions about ambiguous parts.</li>
  <li><b>Validate</b>: acknowledge emotion or intention (“I see this matters to you”).</li>
</ul>

<h2>Example Phrases</h2>
<ul>
  <li>“So if I understand correctly, you mean … right?”</li>
  <li>“Which part is the most frustrating for you?”</li>
  <li>“What do you need from me right now?”</li>
</ul>

<h2>Practice</h2>
<p>In three conversations this week, follow a 2‑1‑1 rule: paraphrase twice, clarify once, validate once. You’ll be surprised how quickly tension drops and solutions appear.</p>
""",
    },

    {
        "id": "a20",
        "title_id": "Konflik di Tim: Menyelaraskan Gaya Kerja",
        "title_en": "Team Conflict: Aligning Work Styles",
        "category_id": "Karier",
        "category_en": "Career",
        "read_time": "9 min",
        "summary_id": "Konflik sering bukan soal niat buruk, tetapi soal gaya kerja yang berbeda.",
        "summary_en": "Conflict is often about mismatched work styles—not bad intentions.",
        "content_id": """
<h2>Sumber Konflik yang Paling Umum</h2>
<p>Di tim, konflik sering muncul dari hal praktis: ekspektasi tidak jelas, definisi “selesai” berbeda, ritme kerja berbeda, dan cara komunikasi berbeda. Orang detail bisa frustrasi pada orang cepat; orang cepat bisa frustrasi pada orang detail.</p>

<h2>Checklist Diagnosa</h2>
<ul>
  <li>Apakah tujuan dan prioritas sudah disepakati?</li>
  <li>Apakah ada definisi done dan quality bar?</li>
  <li>Apakah deadline dan ownership jelas?</li>
  <li>Apakah channel komunikasi tepat (sinkron vs tertulis)?</li>
</ul>

<h2>Solusi Praktis</h2>
<ol>
  <li>Buat dokumentasi 1 halaman: tujuan, peran, milestone, risiko.</li>
  <li>Gunakan meeting singkat: agenda 3 poin + keputusan + action items.</li>
  <li>Review rutin 15 menit untuk menyelaraskan, bukan menunggu meledak.</li>
</ol>

<h2>Latihan</h2>
<p>Pilih 1 konflik kecil minggu ini. Ubah pertanyaan dari “siapa salah” menjadi “sistem apa yang kurang jelas?” Lalu perbaiki sistemnya (dokumen, checklist, atau aturan komunikasi).</p>
""",
        "content_en": """
<h2>The Most Common Sources of Conflict</h2>
<p>In teams, conflict often comes from practical gaps: unclear expectations, different definitions of “done,” mismatched work rhythms, and communication style differences. Detail‑oriented people may feel rushed; fast movers may feel slowed down.</p>

<h2>A Quick Diagnostic Checklist</h2>
<ul>
  <li>Have we agreed on goals and priorities?</li>
  <li>Do we have a definition of done and quality bar?</li>
  <li>Are deadlines and ownership clear?</li>
  <li>Is the communication channel appropriate (sync vs written)?</li>
</ul>

<h2>Practical Fixes</h2>
<ol>
  <li>Create a one‑page doc: goals, roles, milestones, risks.</li>
  <li>Run short meetings: 3‑point agenda + decisions + action items.</li>
  <li>Use a 15‑minute weekly alignment review instead of waiting for explosions.</li>
</ol>

<h2>Practice</h2>
<p>Pick one small conflict this week. Shift the question from “who is wrong” to “which system is unclear?” Then fix the system (document, checklist, or communication rule).</p>
""",
    },

    {
        "id": "a21",
        "title_id": "Memilih Karier Berdasarkan Pola Kekuatan, Bukan Label",
        "title_en": "Choosing Careers by Strength Patterns, Not Labels",
        "category_id": "Karier",
        "category_en": "Career",
        "read_time": "9 min",
        "summary_id": "Gunakan hasil tes untuk memahami pola energi dan gaya kerja—bukan menentukan pekerjaan tunggal.",
        "summary_en": "Use tests to understand energy and work patterns—not to pick one “destined” job.",
        "content_id": """
<h2>Mulai dari Pola</h2>
<p>Hasil tes terbaik dipakai untuk mengenali pola: Anda produktif dalam kondisi apa, jenis tugas apa yang memberi energi, dan gaya komunikasi apa yang paling efektif untuk Anda. Ini lebih berguna daripada mencoba mencari “pekerjaan yang cocok untuk tipe X”.</p>

<h2>Metode 3 Lingkaran</h2>
<ul>
  <li><b>Kekuatan</b>: skill yang cepat Anda kuasai dan sering dipuji.</li>
  <li><b>Nilai</b>: hal yang membuat Anda merasa pekerjaan bermakna.</li>
  <li><b>Pasar</b>: kebutuhan dan peluang yang nyata.</li>
</ul>

<h2>Eksperimen Karier</h2>
<p>Daripada langsung pindah jalur, lakukan eksperimen kecil: side project, volunteer, atau tugas lintas fungsi. Catat: apakah energi Anda naik? apakah Anda belajar cepat? apakah hasilnya terasa meaningful?</p>

<h2>Checklist Keputusan</h2>
<ol>
  <li>Apakah role ini memberi ruang pada kekuatan utama saya?</li>
  <li>Apakah saya punya strategi untuk tantangan utamanya?</li>
  <li>Apakah lingkungan (tim, atasan, ritme) mendukung gaya kerja saya?</li>
</ol>
""",
        "content_en": """
<h2>Start with Patterns</h2>
<p>The best use of test results is pattern recognition: when you are productive, which tasks energize you, and which communication style works best. This is more useful than trying to find a single “job for type X.”</p>

<h2>The Three‑Circle Method</h2>
<ul>
  <li><b>Strength</b>: skills you learn fast and get praised for.</li>
  <li><b>Values</b>: what makes work feel meaningful.</li>
  <li><b>Market</b>: real opportunities and demand.</li>
</ul>

<h2>Career Experiments</h2>
<p>Instead of an immediate switch, run small experiments: side projects, volunteering, or cross‑functional tasks. Track: does your energy increase? do you learn quickly? does the work feel meaningful?</p>

<h2>Decision Checklist</h2>
<ol>
  <li>Does this role leverage my core strengths?</li>
  <li>Do I have strategies for the main challenges?</li>
  <li>Does the environment (team, manager, rhythm) support my work style?</li>
</ol>
""",
    },

    {
        "id": "a22",
        "title_id": "Burnout vs Stres Sehat: Tanda dan Pencegahan",
        "title_en": "Burnout vs Healthy Stress: Signs and Prevention",
        "category_id": "Kesehatan Mental",
        "category_en": "Mental Health",
        "read_time": "10 min",
        "summary_id": "Bedakan stres menantang (eustress) dengan burnout yang menguras.",
        "summary_en": "Distinguish challenging stress (eustress) from draining burnout.",
        "content_id": """
<h2>Stres Sehat vs Burnout</h2>
<p>Stres sehat (eustress) biasanya muncul ketika tantangan terasa bermakna dan Anda masih punya kontrol, dukungan, serta pemulihan. Burnout terjadi ketika tekanan berkepanjangan, pemulihan kurang, dan Anda merasa tidak punya kendali atau makna.</p>

<h2>Tanda Burnout</h2>
<ul>
  <li>Lelah kronis yang tidak hilang meski istirahat.</li>
  <li>Sinis, kehilangan motivasi, atau “mati rasa”.</li>
  <li>Performa menurun, sulit fokus, mudah error.</li>
  <li>Gangguan tidur dan pemulihan yang buruk.</li>
</ul>

<h2>Pencegahan yang Realistis</h2>
<ol>
  <li><b>Batas kerja</b>: jam mulai/selesai yang jelas, terutama saat WFH.</li>
  <li><b>Micro‑break</b>: 3–5 menit setiap 60–90 menit untuk reset.</li>
  <li><b>Prioritas</b>: pilih 1–3 hal penting, sisanya “nice to have”.</li>
  <li><b>Komunikasi</b>: minta klarifikasi dan dukungan sebelum kelelahan menumpuk.</li>
</ol>

<p><b>Catatan</b>: jika gejala berat dan berkepanjangan, pertimbangkan konsultasi profesional.</p>
""",
        "content_en": """
<h2>Healthy Stress vs Burnout</h2>
<p>Healthy stress (eustress) often appears when challenges feel meaningful and you still have control, support, and recovery. Burnout happens when pressure is prolonged, recovery is insufficient, and you feel low control or low meaning.</p>

<h2>Burnout Signs</h2>
<ul>
  <li>Chronic exhaustion that does not improve with rest.</li>
  <li>Cynicism, lost motivation, or emotional numbness.</li>
  <li>Declining performance, focus issues, more mistakes.</li>
  <li>Sleep disruption and poor recovery.</li>
</ul>

<h2>Realistic Prevention</h2>
<ol>
  <li><b>Work boundaries</b>: clear start/stop times, especially in remote work.</li>
  <li><b>Micro‑breaks</b>: 3–5 minutes every 60–90 minutes to reset.</li>
  <li><b>Prioritization</b>: choose 1–3 important tasks; treat the rest as “nice to have.”</li>
  <li><b>Communication</b>: ask for clarification and support before overload accumulates.</li>
</ol>

<p><b>Note</b>: if symptoms are severe and persistent, consider professional help.</p>
""",
    },

    {
        "id": "a23",
        "title_id": "Journaling 5 Menit: Refleksi yang Konsisten",
        "title_en": "5‑Minute Journaling: Consistent Reflection",
        "category_id": "Self-Development",
        "category_en": "Self‑Development",
        "read_time": "8 min",
        "summary_id": "Format journaling ringan tapi efektif untuk awareness dan kontrol diri.",
        "summary_en": "A light but effective journaling format for awareness and self‑control.",
        "content_id": """
<h2>Kenapa 5 Menit?</h2>
<p>Journaling sering gagal karena formatnya terlalu panjang. 5 menit adalah kompromi: cukup pendek untuk konsisten, cukup panjang untuk membangun awareness. Anda tidak sedang menulis novel; Anda sedang membangun kebiasaan refleksi.</p>

<h2>Format 3 Pertanyaan</h2>
<ol>
  <li>Apa 1 hal yang berjalan baik hari ini?</li>
  <li>Apa 1 hal yang menantang?</li>
  <li>Apa 1 perbaikan kecil besok?</li>
</ol>

<h2>Manfaat Utama</h2>
<ul>
  <li>Lebih cepat mengenali pemicu stres dan pola reaksi.</li>
  <li>Meningkatkan rasa kontrol: Anda melihat “langkah berikutnya”.</li>
  <li>Membangun self‑compassion: belajar dari hari buruk tanpa menghakimi diri.</li>
</ul>

<h2>Tips Konsistensi</h2>
<p>Pasang journaling setelah kebiasaan lain (misalnya setelah gosok gigi malam). Jika Anda melewatkan 1 hari, lanjutkan besok tanpa rasa bersalah. Targetnya adalah tren, bukan streak sempurna.</p>
""",
        "content_en": """
<h2>Why 5 Minutes?</h2>
<p>Journaling often fails because the format is too long. Five minutes is a good compromise: short enough to stay consistent, long enough to build awareness. You are not writing a novel—you are building a reflection habit.</p>

<h2>The 3‑Question Format</h2>
<ol>
  <li>What is one thing that went well today?</li>
  <li>What is one challenge I faced?</li>
  <li>What is one small improvement for tomorrow?</li>
</ol>

<h2>Key Benefits</h2>
<ul>
  <li>Spot stress triggers and reaction patterns faster.</li>
  <li>Increase control by identifying “the next step.”</li>
  <li>Build self‑compassion: learn from bad days without self‑judgment.</li>
</ul>

<h2>Consistency Tips</h2>
<p>Anchor journaling after another habit (e.g., after brushing teeth). If you miss one day, continue the next day without guilt. The goal is the trend, not a perfect streak.</p>
""",
    },

    {
        "id": "a24",
        "title_id": "Memberi & Menerima Feedback yang Efektif",
        "title_en": "Giving and Receiving Feedback Effectively",
        "category_id": "Karier",
        "category_en": "Career",
        "read_time": "9 min",
        "summary_id": "Feedback fokus pada perilaku dan dampaknya—bukan menyerang karakter.",
        "summary_en": "Feedback should target behavior and impact—not personal character.",
        "content_id": """
<h2>Prinsip Utama</h2>
<p>Feedback yang baik fokus pada perilaku yang bisa diubah, bukan menyerang identitas. Tujuannya adalah perbaikan dan pembelajaran. Saat feedback aman, orang lebih mudah menerima dan bertindak.</p>

<h2>Memberi Feedback: SBI</h2>
<ul>
  <li><b>Situation</b>: kapan/di mana terjadi.</li>
  <li><b>Behavior</b>: perilaku spesifik yang terlihat.</li>
  <li><b>Impact</b>: dampaknya pada tim/hasil.</li>
</ul>
<p>Contoh: “Di meeting tadi (S), kamu memotong pembicaraan (B), jadi beberapa ide tidak terdengar (I).” Tambahkan permintaan: “Bisa kita coba tunggu 10 detik sebelum interupsi?”</p>

<h2>Menerima Feedback</h2>
<ol>
  <li>Dengar sampai selesai, lalu ringkas kembali untuk memastikan akurat.</li>
  <li>Tanya contoh spesifik dan ekspektasi yang diinginkan.</li>
  <li>Pilih 1 aksi perbaikan yang terukur selama 1-2 minggu.</li>
</ol>

<h2>Latihan</h2>
<p>Pilih satu feedback terakhir yang Anda terima. Ubah menjadi action plan 3 langkah. Jadwalkan review singkat setelah 7 hari untuk melihat progres.</p>
""",
        "content_en": """
<h2>Core Principle</h2>
<p>Good feedback targets changeable behavior, not personal identity. The goal is improvement and learning. When feedback feels safe, people are more likely to accept it and take action.</p>

<h2>Giving Feedback: SBI</h2>
<ul>
  <li><b>Situation</b>: when/where it happened.</li>
  <li><b>Behavior</b>: the specific observable behavior.</li>
  <li><b>Impact</b>: the effect on the team or outcome.</li>
</ul>
<p>Example: “In today's meeting (S), you interrupted several times (B), so some ideas were not heard (I).” Add a request: “Can we try waiting 10 seconds before jumping in?”</p>

<h2>Receiving Feedback</h2>
<ol>
  <li>Listen fully, then summarize to confirm accuracy.</li>
  <li>Ask for specific examples and desired expectations.</li>
  <li>Pick one measurable improvement action for 1-2 weeks.</li>
</ol>

<h2>Practice</h2>
<p>Choose one recent feedback you received. Turn it into a 3-step action plan. Schedule a short review after 7 days to check progress.</p>
""",
    },

    {
        "id": "a25",
        "title_id": "Privasi Data: Apa yang Aman Disimpan di Aplikasi Offline",
        "title_en": "Data Privacy: What's Safe to Store in an Offline App",
        "category_id": "Dasar",
        "category_en": "Fundamentals",
        "read_time": "9 min",
        "summary_id": "Pahami data yang disimpan Characterify dan cara menjaga privasi di perangkat Anda.",
        "summary_en": "Understand what Characterify stores and how to protect privacy on your device.",
        "content_id": """
<h2>Offline-First</h2>
<p>Characterify dirancang offline-first: data disimpan secara lokal di komputer Anda (SQLite). Ini membantu privasi karena data tidak otomatis dikirim ke server. Namun, keamanan tetap bergantung pada keamanan perangkat Anda.</p>

<h2>Apa yang Disimpan</h2>
<ul>
  <li><b>Akun</b>: nama, email, password hash (bukan password asli).</li>
  <li><b>History tes</b>: jenis tes, skor ringkas, hasil, waktu.</li>
  <li><b>Preferensi</b>: tema, bahasa, dan pengingat offline.</li>
  <li><b>Aktivitas belajar</b>: status dibaca/bookmark (opsional).</li>
</ul>

<h2>Tips Privasi Praktis</h2>
<ol>
  <li>Gunakan password akun yang kuat dan jangan dibagikan.</li>
  <li>Gunakan user account OS terpisah jika perangkat dipakai bersama.</li>
  <li>Manfaatkan fitur <b>Export</b> dan <b>Clear History</b> saat diperlukan.</li>
  <li>Backup file database hanya di lokasi yang aman.</li>
</ol>

<p><b>Disclaimer</b>: aplikasi ini bukan alat diagnosis klinis dan tidak menggantikan konsultasi profesional.</p>
""",
        "content_en": """
<h2>Offline‑First</h2>
<p>Characterify is offline‑first: data is stored locally on your computer (SQLite). This supports privacy because nothing is automatically sent to a server. However, security still depends on your device security.</p>

<h2>What Is Stored</h2>
<ul>
  <li><b>Account</b>: name, email, password hash (not the raw password).</li>
  <li><b>Test history</b>: test type, summary scores, result, timestamp.</li>
  <li><b>Preferences</b>: theme, language, and offline reminders.</li>
  <li><b>Learning activity</b>: read/bookmark status (optional).</li>
</ul>

<h2>Practical Privacy Tips</h2>
<ol>
  <li>Use a strong account password and do not share it.</li>
  <li>Use separate OS user accounts if the device is shared.</li>
  <li>Use <b>Export</b> and <b>Clear History</b> when needed.</li>
  <li>Back up the database file only to secure locations.</li>
</ol>

<p><b>Disclaimer</b>: this app is not a clinical diagnostic tool and does not replace professional consultation.</p>
""",
    },
    
]


def get_articles(lang: str = "id") -> List[Dict]:
    """Return localized article list.

    The UI uses this to render cards and article content.
    """

    lang = "en" if lang == "en" else "id"
    out: List[Dict] = []
    for a in ARTICLES:
        out.append(
            {
                "id": a["id"],
                "title": a["title_en"] if lang == "en" else a["title_id"],
                "category": a["category_en"] if lang == "en" else a["category_id"],
                "read_time": a["read_time"],
                "summary": a["summary_en"] if lang == "en" else a["summary_id"],
                "content": _augment_if_short(
                    title=(a["title_en"] if lang == "en" else a["title_id"]),
                    html=(a["content_en"] if lang == "en" else a["content_id"]),
                    lang=lang,
                ),
            }
        )
    return out


def get_article(article_id: str, lang: str = "id") -> Dict:
    """Get a single localized article by id."""

    lang = "en" if lang == "en" else "id"
    a = next((x for x in ARTICLES if x["id"] == article_id), None)
    if not a:
        return {}
    return {
        "id": a["id"],
        "title": a["title_en"] if lang == "en" else a["title_id"],
        "category": a["category_en"] if lang == "en" else a["category_id"],
        "read_time": a["read_time"],
        "summary": a["summary_en"] if lang == "en" else a["summary_id"],
        "content": _augment_if_short(
            title=(a["title_en"] if lang == "en" else a["title_id"]),
            html=(a["content_en"] if lang == "en" else a["content_id"]),
            lang=lang,
        ),
    }
