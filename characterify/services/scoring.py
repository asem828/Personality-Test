# characterify/services/scoring.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from characterify.data.mbti_questions import questions as MBTI_QUESTIONS
from characterify.data.ocean_questions import ocean_questions as OCEAN_QUESTIONS
from characterify.data.enneagram_questions import enneagram_questions as ENNEAGRAM_QUESTIONS
from characterify.data.temperaments_questions import temperaments_questions as TEMPERAMENT_QUESTIONS


@dataclass(frozen=True)
class QuestionItem:
    trait: str
    text: str


@dataclass(frozen=True)
class TestDefinition:
    id: str
    title: str
    subtitle: str
    description: str
    instructions: List[str]
    questions: List[QuestionItem]
    scale_type: str  # "likert5"


class ScoringService:
    """Provides test definitions + scoring logic + long per-type narratives."""

    def get_tests(self) -> List[TestDefinition]:
        return [
            TestDefinition(
                id="mbti",
                title="MBTI",
                subtitle="Myers-Briggs Type Indicator",
                description=(
                    "Tes MBTI dirancang untuk membantu Anda memahami kecenderungan kepribadian yang "
                    "memengaruhi cara Anda berpikir, berinteraksi, dan mengambil keputusan. Hasilnya bukan "
                    "penilaian benar/salah, melainkan peta preferensi alami Anda."
                ),
                instructions=[
                    "Tidak ada jawaban benar atau salah. Pilih jawaban yang paling sesuai dengan diri Anda.",
                    "Jawablah secara jujur dan spontan, jangan terlalu lama berpikir.",
                    "Fokus pada kebiasaan umum Anda, bukan situasi khusus.",
                    "Waktu pengerjaan: ±10–15 menit.",
                ],
                questions=[QuestionItem(trait=t, text=q) for t, q in MBTI_QUESTIONS],
                scale_type="likert5",
            ),
            TestDefinition(
                id="ocean",
                title="Big Five (OCEAN)",
                subtitle="Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism",
                description=(
                    "Big Five (OCEAN) memetakan kepribadian Anda dalam 5 dimensi utama. Kerangka ini membantu "
                    "memahami gaya kerja, relasi, preferensi komunikasi, serta cara Anda merespons tekanan."
                ),
                instructions=[
                    "Gunakan skala 1–5 sesuai tingkat kesesuaian dengan diri Anda.",
                    "Jawab berdasarkan kebiasaan umum, bukan hari ini saja.",
                    "Tidak ada jawaban benar/salah.",
                    "Durasi: ±8–12 menit.",
                ],
                questions=[QuestionItem(trait=t, text=q) for t, q in OCEAN_QUESTIONS],
                scale_type="likert5",
            ),
            TestDefinition(
                id="enneagram",
                title="Enneagram",
                subtitle="9 Tipe Motivasi Inti",
                description=(
                    "Enneagram membantu Anda memahami motivasi inti, pola emosi, dan strategi bertahan. "
                    "Cocok untuk refleksi diri: mengenali pemicu, kebutuhan, dan kebiasaan berulang."
                ),
                instructions=[
                    "Jawab spontan: pilih yang paling menggambarkan diri Anda.",
                    "Fokus pada pola yang sering terjadi.",
                    "Gunakan skala 1–5.",
                    "Durasi: ±8–12 menit.",
                ],
                questions=[QuestionItem(trait=t, text=q) for t, q in ENNEAGRAM_QUESTIONS],
                scale_type="likert5",
            ),
            TestDefinition(
                id="temperament",
                title="4 Temperaments",
                subtitle="Sanguine, Choleric, Phlegmatic, Melancholic",
                description=(
                    "Tes Temperament memetakan kecenderungan energi dan gaya interaksi Anda. Hasilnya "
                    "berguna untuk komunikasi, kerja tim, dan manajemen diri."
                ),
                instructions=[
                    "Jawab dengan jujur dan konsisten.",
                    "Gunakan skala 1–5.",
                    "Tidak ada jawaban benar/salah.",
                    "Durasi: ±5–8 menit.",
                ],
                questions=[QuestionItem(trait=t, text=q) for t, q in TEMPERAMENT_QUESTIONS],
                scale_type="likert5",
            ),
        ]

    # ---------------------------
    # Scoring entrypoint
    # ---------------------------
    def score_test(self, test_id: str, answers: Dict[int, int]) -> Dict[str, Any]:
        if test_id == "mbti":
            return self._score_mbti(answers)
        if test_id == "ocean":
            return self._score_ocean(answers)
        if test_id == "enneagram":
            return self._score_enneagram(answers)
        if test_id == "temperament":
            return self._score_temperament(answers)
        raise ValueError(f"Unknown test id: {test_id}")

    # ---------------------------
    # MBTI
    # ---------------------------
    def _score_mbti(self, answers: Dict[int, int]) -> Dict[str, Any]:
        scores = {k: 0 for k in ["I", "E", "N", "S", "T", "F", "P", "J"]}
        for i, (trait, _) in enumerate(MBTI_QUESTIONS):
            scores[trait] += int(answers.get(i, 0))

        result = ""
        result += "I" if scores["I"] >= scores["E"] else "E"
        result += "N" if scores["N"] >= scores["S"] else "S"
        result += "T" if scores["T"] >= scores["F"] else "F"
        result += "P" if scores["P"] >= scores["J"] else "J"

        dimensions = [
            ("I", "E", "Introvert", "Extrovert"),
            ("N", "S", "Intuitive", "Sensing"),
            ("T", "F", "Thinking", "Feeling"),
            ("P", "J", "Perceiving", "Judging"),
        ]

        dim_percentages: List[Dict[str, Any]] = []
        for a, b, name_a, name_b in dimensions:
            total = scores[a] + scores[b] or 1
            pct_a = scores[a] / total * 100
            pct_b = scores[b] / total * 100
            dim_percentages.append(
                {"a": a, "b": b, "name_a": name_a, "name_b": name_b, "pct_a": pct_a, "pct_b": pct_b}
            )

        content = self._mbti_content(result, dim_percentages)
        return {
            "test_id": "mbti",
            "result_type": result,
            "scores": scores,
            "percentages": dim_percentages,
            "chart_kind": "mbti_stacked",
            "content": content,
        }

    def _mbti_content(self, code: str, dims: List[Dict[str, Any]]) -> Dict[str, Any]:
        type_names = {
            "ISTJ": ("Logistician", "Pribadi yang terstruktur, realistis, dan bertanggung jawab."),
            "ISFJ": ("Defender", "Hangat, teliti, dan sangat mengutamakan stabilitas serta kepedulian."),
            "INFJ": ("Advocate", "Visioner, idealis, dan peka terhadap makna serta nilai."),
            "INTJ": ("Strategist", "Analitis, mandiri, dan berorientasi sistem serta perbaikan."),
            "ISTP": ("Virtuoso", "Praktis, tenang, dan unggul dalam pemecahan masalah di lapangan."),
            "ISFP": ("Adventurer", "Sensitif, fleksibel, dan mengekspresikan diri dengan autentik."),
            "INFP": ("Mediator", "Reflektif, empatik, dan dipandu nilai pribadi yang kuat."),
            "INTP": ("Thinker", "Rasa ingin tahu tinggi, logis, dan suka memahami konsep mendalam."),
            "ESTP": ("Entrepreneur", "Berani, cepat, dan nyaman mengambil keputusan dalam dinamika."),
            "ESFP": ("Entertainer", "Energik, sosial, dan menciptakan suasana positif."),
            "ENFP": ("Campaigner", "Kreatif, antusias, dan mudah terhubung dengan banyak orang."),
            "ENTP": ("Debater", "Inovatif, argumentatif sehat, dan suka mengeksplorasi ide baru."),
            "ESTJ": ("Executive", "Tegas, terorganisir, dan fokus pada hasil serta ketertiban."),
            "ESFJ": ("Consul", "Ramah, suportif, dan menjaga harmoni dalam komunitas."),
            "ENFJ": ("Protagonist", "Inspiratif, empatik, dan memiliki dorongan untuk memberi dampak."),
            "ENTJ": ("Commander", "Visioner, tegas, dan nyaman memimpin arah strategis."),
        }

        # 1 paragraf panjang PER TYPE (ini yang kamu minta)
        type_long: Dict[str, str] = {
            "INTP": (
                "Sebagai INTP, Anda cenderung berpikir dengan cara yang konseptual dan analitis—tertarik pada pola, teori, "
                "dan penjelasan yang ‘masuk akal’ secara logis. Anda biasanya menikmati mengeksplorasi ide dari berbagai sisi, "
                "menguji asumsi, dan memperbaiki cara berpikir sampai terasa konsisten. Dalam pekerjaan atau belajar, INTP sering "
                "unggul ketika diberi ruang untuk riset, problem-solving, dan merancang solusi yang elegan. Tantangan yang umum "
                "muncul adalah kecenderungan untuk menunda eksekusi karena ingin pemahaman yang sempurna, atau kehilangan energi "
                "ketika harus mengikuti prosedur yang terasa tidak rasional. Secara sosial, Anda bisa hangat dan lucu, namun tetap "
                "butuh waktu sendiri untuk ‘mengisi ulang’ dan memproses informasi. Kunci berkembang bagi INTP adalah menyeimbangkan "
                "kedalaman analisis dengan kebiasaan eksekusi kecil yang konsisten (misalnya time-box), serta melatih komunikasi yang "
                "lebih eksplisit agar ide-ide Anda mudah dipahami orang lain."
            ),
            "INTJ": (
                "Sebagai INTJ, Anda cenderung strategis, sistematis, dan berorientasi perbaikan. Anda biasanya melihat pola besar, "
                "menyusun rencana jangka panjang, lalu memecahnya menjadi langkah yang efisien. INTJ sering nyaman bekerja mandiri, "
                "menganalisis masalah kompleks, dan membuat keputusan berbasis logika serta tujuan. Dalam tim, Anda cenderung dihargai "
                "karena ketajaman analisis dan kemampuan membangun struktur, namun dapat dianggap terlalu ‘to the point’ bila tidak "
                "diimbangi empati komunikasi. Tantangan INTJ sering terkait perfeksionisme, standar tinggi, dan kesabaran saat orang lain "
                "bergerak lebih lambat atau kurang sistematis. Di bawah tekanan, Anda bisa menjadi lebih kaku atau terlalu mengontrol. "
                "Pengembangan terbaik bagi INTJ adalah melatih fleksibilitas (iterasi cepat), meningkatkan kemampuan menjelaskan alasan "
                "di balik keputusan, dan membangun kebiasaan kolaborasi yang membuat orang lain merasa dilibatkan."
            ),
            "INFJ": (
                "Sebagai INFJ, Anda cenderung memadukan intuisi yang mendalam dengan kepedulian terhadap nilai dan manusia. Anda biasanya "
                "mencari makna di balik kejadian, membaca dinamika emosional, dan ingin memberi dampak positif. INFJ sering unggul dalam "
                "peran yang melibatkan mentoring, perencanaan yang bermakna, menulis, atau memfasilitasi perubahan yang terarah. Anda "
                "mungkin terlihat tenang, namun memiliki dunia batin yang kaya dan standar nilai yang kuat. Tantangan INFJ adalah mudah "
                "lelah karena terlalu banyak menyerap emosi orang lain, atau menekan kebutuhan pribadi demi harmoni. Dalam tekanan, Anda "
                "bisa overthinking, menarik diri, atau merasa kecewa ketika realitas tidak sesuai ideal. Kunci berkembang bagi INFJ adalah "
                "memasang batas sehat (boundaries), menyampaikan kebutuhan secara jelas, dan mempraktikkan keseimbangan antara idealisme "
                "dan aksi kecil yang konsisten."
            ),
            "INFP": (
                "Sebagai INFP, Anda cenderung berorientasi nilai, empatik, dan autentik. Anda biasanya memilih keputusan yang selaras "
                "dengan prinsip pribadi dan memiliki sensitivitas tinggi terhadap makna, keadilan, serta emosi. INFP sering unggul dalam "
                "karya kreatif, peran yang membutuhkan empati, atau pekerjaan yang memberi ruang untuk refleksi dan kualitas relasi. "
                "Tantangan yang umum adalah kesulitan menghadapi konflik, kecenderungan ragu karena ingin ‘tepat secara nilai’, atau "
                "menunda tugas yang terasa tidak bermakna. Dalam tim, Anda bisa menjadi penyeimbang yang bijak, namun perlu belajar "
                "mengkomunikasikan batasan dan preferensi kerja agar tidak disalahpahami. Pengembangan terbaik bagi INFP adalah membangun "
                "struktur ringan (rutinitas, time-box), melatih keberanian menyampaikan pendapat, dan membiasakan ‘selesai dulu’ sebelum "
                "mengejar sempurna."
            ),
            "ISTJ": (
                "Sebagai ISTJ, Anda cenderung praktis, terstruktur, dan berorientasi tanggung jawab. Anda biasanya percaya pada "
                "konsistensi, aturan yang jelas, dan cara kerja yang terbukti efektif. ISTJ sering unggul dalam peran yang membutuhkan "
                "ketelitian, kepatuhan prosedur, manajemen operasional, atau pengelolaan sistem yang stabil. Anda menghargai keandalan "
                "dan cenderung menepati komitmen. Tantangan ISTJ dapat muncul saat perubahan mendadak, ambiguitas, atau ketika harus "
                "mengandalkan intuisi tanpa data yang cukup. Dalam tekanan, Anda bisa menjadi lebih kaku atau kritis. Kunci berkembang "
                "bagi ISTJ adalah menambah ruang fleksibilitas (mis. rencana alternatif), melatih komunikasi yang lebih hangat, dan "
                "mencoba melihat ‘mengapa’ di balik perubahan agar adaptasi terasa lebih masuk akal."
            ),
            "ISFJ": (
                "Sebagai ISFJ, Anda cenderung hangat, teliti, dan berorientasi pelayanan. Anda biasanya memperhatikan detail yang "
                "membuat orang lain nyaman, menjaga stabilitas, dan siap membantu secara konsisten. ISFJ sering unggul dalam peran "
                "yang membutuhkan ketekunan, perhatian pada kebutuhan orang, serta kerja yang rapi dan berkelanjutan. Anda menghargai "
                "hubungan yang aman dan lingkungan yang dapat diprediksi. Tantangan ISFJ adalah kecenderungan memikul terlalu banyak "
                "tanggung jawab, sulit berkata ‘tidak’, atau menunda mengungkapkan kebutuhan pribadi. Dalam tekanan, Anda bisa menjadi "
                "lebih sensitif terhadap kritik atau merasa tidak dihargai. Pengembangan terbaik bagi ISFJ adalah melatih batas sehat, "
                "mendelegasikan, dan mengekspresikan kebutuhan dengan cara yang tenang namun jelas."
            ),
            "ISTP": (
                "Sebagai ISTP, Anda cenderung tenang, pragmatis, dan fokus pada pemecahan masalah yang nyata. Anda biasanya cepat "
                "membaca situasi, mengurai masalah menjadi bagian-bagian kecil, lalu memperbaikinya dengan cara yang efisien. ISTP "
                "sering unggul pada peran yang membutuhkan troubleshooting, eksperimen, dan adaptasi cepat di lapangan. Anda menghargai "
                "kebebasan dan tidak suka terlalu banyak aturan yang menghambat. Tantangan ISTP dapat muncul saat harus berurusan dengan "
                "emosi yang kompleks atau komunikasi yang terlalu ‘berputar-putar’. Dalam tekanan, Anda bisa menarik diri atau menjadi "
                "terlalu blunt. Kunci berkembang bagi ISTP adalah melatih komunikasi yang lebih eksplisit, menyampaikan update proses, "
                "serta membangun kebiasaan follow-through untuk menyelesaikan hal-hal yang monoton namun penting."
            ),
            "ISFP": (
                "Sebagai ISFP, Anda cenderung peka, fleksibel, dan mengekspresikan diri dengan cara yang autentik. Anda biasanya "
                "memperhatikan pengalaman saat ini, kualitas estetika, dan nilai personal dalam tindakan sehari-hari. ISFP sering unggul "
                "dalam peran yang membutuhkan kepekaan, kreativitas praktis, serta pendekatan yang humanis. Anda cenderung tidak suka "
                "dipaksa dan lebih nyaman bergerak dengan ritme alami. Tantangan ISFP adalah kesulitan menghadapi kritik keras, menghindari "
                "konflik, atau menunda keputusan besar karena ingin menjaga perasaan semua pihak. Dalam tekanan, Anda bisa menarik diri "
                "atau kehilangan motivasi. Pengembangan terbaik bagi ISFP adalah membangun struktur sederhana (jadwal ringan), melatih "
                "asertif, dan membuat target kecil yang realistis agar bakat dan nilai Anda terwujud menjadi hasil nyata."
            ),
            "ENTP": (
                "Sebagai ENTP, Anda cenderung inovatif, cepat menangkap ide, dan menikmati eksplorasi kemungkinan. Anda biasanya "
                "tertarik pada diskusi, debat sehat, serta menemukan cara baru yang lebih efektif. ENTP sering unggul dalam brainstorming, "
                "strategi, komunikasi persuasif, dan memecahkan masalah dengan pendekatan kreatif. Anda nyaman menghadapi perubahan dan "
                "sering melihat peluang saat orang lain melihat hambatan. Tantangan ENTP adalah kecenderungan berpindah-pindah fokus, "
                "menunda penyelesaian karena tertarik hal baru, atau terlihat terlalu menantang bagi orang yang sensitif. Dalam tekanan, "
                "Anda bisa jadi impulsif atau terlalu argumentatif. Kunci berkembang bagi ENTP adalah disiplin eksekusi (time-box, checklist), "
                "melatih empati dalam debat, dan menutup keputusan kecil agar ide-ide brilian Anda benar-benar menjadi output."
            ),
            "ENTJ": (
                "Sebagai ENTJ, Anda cenderung tegas, visioner, dan berorientasi hasil. Anda biasanya nyaman memimpin, menetapkan arah, "
                "dan membuat sistem yang meningkatkan performa. ENTJ sering unggul dalam perencanaan strategis, pengambilan keputusan, "
                "serta menggerakkan tim menuju target. Anda menghargai efisiensi dan keberanian mengambil tanggung jawab. Tantangan ENTJ "
                "sering terkait kesabaran, kecenderungan menekan saat standar tidak terpenuhi, atau mengabaikan aspek emosional yang sebenarnya "
                "penting untuk keberlanjutan tim. Dalam tekanan, Anda bisa menjadi terlalu dominan atau sulit menerima masukan. Pengembangan "
                "terbaik bagi ENTJ adalah melatih kepemimpinan yang lebih coaching-oriented: mendengar, mengajak kolaborasi, memberi ruang tim "
                "mengambil peran, dan menyeimbangkan kecepatan dengan kualitas relasi."
            ),
            "ENFJ": (
                "Sebagai ENFJ, Anda cenderung hangat, inspiratif, dan peka terhadap kebutuhan orang lain. Anda biasanya mudah membangun "
                "kepercayaan, menyatukan orang, dan mendorong pertumbuhan bersama. ENFJ sering unggul dalam peran yang melibatkan leadership "
                "humanis, mentoring, komunikasi, atau manajemen tim. Anda mampu membaca dinamika sosial dan mengarahkan energi kelompok ke tujuan "
                "yang bermakna. Tantangan ENFJ adalah terlalu memikul beban emosional orang lain, sulit memprioritaskan kebutuhan diri, atau "
                "menjadi sangat kecewa saat harmoni terganggu. Dalam tekanan, Anda bisa overhelping atau overthinking tentang persepsi orang. "
                "Kunci berkembang bagi ENFJ adalah menetapkan batas sehat, mendelegasikan, dan menjaga keseimbangan antara empati dan ketegasan "
                "agar dampak Anda tetap berkelanjutan."
            ),
            "ENFP": (
                "Sebagai ENFP, Anda cenderung antusias, kreatif, dan mudah terhubung dengan banyak orang. Anda biasanya melihat peluang, "
                "membaca potensi, dan menghidupkan suasana melalui ide serta energi positif. ENFP sering unggul dalam komunikasi, kreativitas, "
                "membangun komunitas, dan menginspirasi perubahan. Anda menghargai kebebasan dan makna, sehingga bekerja paling baik ketika "
                "tujuan terasa ‘nyambung’ dengan nilai Anda. Tantangan ENFP adalah menjaga konsistensi, menyelesaikan hal-hal monoton, atau "
                "menunda keputusan ketika terlalu banyak opsi. Dalam tekanan, Anda bisa terdistraksi atau emosional. Pengembangan terbaik bagi "
                "ENFP adalah membangun sistem sederhana (prioritas harian, time-box), melatih fokus 1–2 tujuan utama, dan membuat ritme review "
                "agar ide-ide Anda benar-benar menjadi progress."
            ),
            "ESTP": (
                "Sebagai ESTP, Anda cenderung cepat, berani, dan responsif terhadap situasi. Anda biasanya nyaman membuat keputusan praktis "
                "dengan cepat, mengambil peluang, dan bertindak saat dibutuhkan. ESTP sering unggul dalam peran yang dinamis: negosiasi, "
                "penjualan, krisis, operasional lapangan, atau aktivitas yang membutuhkan adaptasi cepat. Anda menikmati tantangan dan "
                "cenderung memecahkan masalah lewat aksi. Tantangan ESTP adalah kecenderungan mengambil risiko tanpa pertimbangan jangka panjang, "
                "kurang sabar pada detail, atau terlihat terlalu blak-blakan. Dalam tekanan, Anda bisa impulsif atau mengabaikan perasaan orang. "
                "Kunci berkembang bagi ESTP adalah melatih pause sebelum keputusan besar, menambah kebiasaan evaluasi (review), dan membangun "
                "struktur minimum agar kecepatan Anda menghasilkan outcome yang lebih stabil."
            ),
            "ESFP": (
                "Sebagai ESFP, Anda cenderung ramah, ekspresif, dan membawa energi positif ke lingkungan. Anda biasanya menikmati interaksi, "
                "membuat orang merasa nyaman, dan hidup di momen ‘sekarang’. ESFP sering unggul dalam peran yang melibatkan komunikasi, pelayanan, "
                "presentasi, event, atau pekerjaan yang membutuhkan keterampilan sosial. Anda cepat membaca suasana dan dapat menjadi penghubung yang "
                "membuat tim lebih hangat. Tantangan ESFP adalah konsistensi dan fokus jangka panjang, terutama ketika tugas terasa repetitif atau "
                "tidak menarik. Dalam tekanan, Anda bisa menghindari masalah atau mencari distraksi. Pengembangan terbaik bagi ESFP adalah membangun "
                "rutinitas ringan (3 prioritas harian), melatih pengelolaan waktu, dan membuat target yang jelas agar energi Anda tidak hanya terasa—"
                "tetapi menghasilkan hasil yang terukur."
            ),
            "ESTJ": (
                "Sebagai ESTJ, Anda cenderung tegas, terorganisir, dan fokus pada hasil. Anda biasanya menyukai struktur, aturan yang jelas, dan "
                "proses yang efisien. ESTJ sering unggul dalam manajemen, operasional, koordinasi tim, serta memastikan standar dan timeline terpenuhi. "
                "Anda nyaman mengambil keputusan dan menetapkan ekspektasi. Tantangan ESTJ bisa muncul ketika orang lain tidak sejalan dengan standar Anda, "
                "atau saat situasi memerlukan fleksibilitas dan empati lebih tinggi. Dalam tekanan, Anda bisa terlihat terlalu keras atau mengontrol. "
                "Pengembangan terbaik bagi ESTJ adalah melatih komunikasi yang lebih coaching, memberi ruang diskusi, dan menyeimbangkan ‘tegas’ dengan "
                "‘mendengar’ agar kepemimpinan Anda tetap efektif sekaligus diterima."
            ),
            "ESFJ": (
                "Sebagai ESFJ, Anda cenderung suportif, kooperatif, dan menjaga harmoni sosial. Anda biasanya memperhatikan kebutuhan orang, "
                "mengorganisir kegiatan, serta memastikan semua pihak merasa dilibatkan. ESFJ sering unggul dalam peran pelayanan, koordinasi, "
                "komunitas, HR, atau lingkungan yang membutuhkan relasi kuat dan keteraturan. Anda nyaman dengan rutinitas yang jelas dan suka "
                "melihat orang berkembang. Tantangan ESFJ adalah kecenderungan terlalu memikirkan pendapat orang, sulit berkata ‘tidak’, atau "
                "menghindari konflik yang sebenarnya perlu diselesaikan. Dalam tekanan, Anda bisa menjadi sensitif terhadap kritik. Pengembangan "
                "terbaik bagi ESFJ adalah membangun batas sehat, melatih asertif, dan memisahkan ‘kritik terhadap tindakan’ dari ‘nilai diri’ "
                "agar tetap stabil dan percaya diri."
            ),
        }

        # Fallback untuk tipe yang belum didefinisikan (harusnya semua ada)
        if code not in type_long:
            type_long[code] = (
                "Tipe Anda menunjukkan kombinasi preferensi yang unik. Gunakan laporan ini sebagai peta kebiasaan: bagaimana Anda mengisi energi, "
                "memproses informasi, mengambil keputusan, dan mengatur ritme kerja. Perhatikan bagian kekuatan, tantangan, dan saran pengembangan "
                "untuk langkah yang paling relevan bagi Anda."
            )

        name_en, tagline = type_names.get(code, (code, ""))

        pref_long = {
            "I": ("Introvert", "Energi cenderung pulih lewat waktu pribadi, fokus mendalam, dan ruang berpikir."),
            "E": ("Extrovert", "Energi cenderung pulih lewat interaksi, diskusi, dan stimulasi sosial."),
            "S": ("Sensing", "Cenderung memproses informasi lewat fakta, detail nyata, dan pengalaman langsung."),
            "N": ("Intuitive", "Cenderung memproses informasi lewat pola, ide, kemungkinan, dan makna di balik peristiwa."),
            "T": ("Thinking", "Lebih nyaman menilai keputusan lewat logika, konsistensi, dan kejelasan kriteria."),
            "F": ("Feeling", "Lebih nyaman menilai keputusan lewat nilai, empati, serta dampak pada orang lain."),
            "P": ("Perceiving", "Menyukai fleksibilitas, eksplorasi opsi, dan menyesuaikan strategi saat berjalan."),
            "J": ("Judging", "Menyukai struktur, rencana, kepastian, dan penutupan keputusan yang jelas."),
        }

        def _dominance(d: Dict[str, Any]) -> Tuple[str, float, str]:
            if d["pct_a"] >= d["pct_b"]:
                return d["a"], d["pct_a"], d["name_a"]
            return d["b"], d["pct_b"], d["name_b"]

        pref_paras: List[str] = []
        for p in list(code):
            label, desc = pref_long.get(p, (p, p))
            pref_paras.append(f"- **{p} ({label})**: {desc}")

        dim_insights: List[str] = []
        for d in dims:
            win_letter, win_pct, win_name = _dominance(d)
            lose_letter = d["b"] if win_letter == d["a"] else d["a"]
            lose_name = d["name_b"] if win_letter == d["a"] else d["name_a"]
            dim_insights.append(
                f"**{d['name_a']} vs {d['name_b']}**: "
                f"lebih condong ke **{win_name} ({win_letter})** sekitar **{win_pct:.0f}%** "
                f"(dibanding {lose_name} / {lose_letter})."
            )

        intro_framework = (
            "MBTI memetakan **preferensi psikologis**—bukan kemampuan, bukan kecerdasan, dan bukan nilai moral. "
            "Tipe Anda bukan ‘kotak’ yang membatasi, melainkan peta kebiasaan yang membantu Anda memahami pola alami. "
            "Jika persentase pada dimensi berdekatan, Anda cenderung fleksibel; jika jauh, Anda biasanya sangat nyaman "
            "pada satu sisi dan mungkin perlu latihan sadar untuk menyeimbangkan sisi lain."
        )

        strengths = [
            "Memiliki pola kerja khas yang dapat diandalkan ketika lingkungan mendukung preferensi Anda.",
            "Cenderung memahami masalah secara konsisten sehingga keputusan terasa ‘make sense’ bagi Anda.",
            "Berpotensi kuat dalam kolaborasi jika ekspektasi peran dan ritme komunikasi jelas.",
            "Dapat berkembang cepat ketika mendapat umpan balik yang konkret dan ruang untuk memperbaiki proses.",
        ]

        challenges = [
            "Blind spot: terlalu nyaman pada preferensi sendiri sehingga mengabaikan sinyal penting dari gaya yang berbeda.",
            "Pada kondisi lelah/tekanan, respons bisa ekstrem (mis. menarik diri, overcontrol, overthinking, atau people-pleasing).",
            "Konflik gaya komunikasi bisa muncul jika tidak ada kesepakatan cara kerja (detail vs big picture, cepat vs terstruktur).",
            "Risiko mis-komunikasi: menganggap orang lain memproses informasi seperti Anda (padahal berbeda).",
        ]

        communication = [
            "Gunakan format jelas: konteks → tujuan → permintaan → batas waktu (jika ada).",
            "Tanyakan preferensi lawan bicara: butuh detail atau garis besar? diskusi dulu atau langsung aksi?",
            "Buat ruang klarifikasi: ulangi ringkas apa yang dipahami sebelum eksekusi.",
            "Jika konflik, pisahkan ‘fakta’ dan ‘interpretasi’ lalu sepakati langkah berikutnya.",
        ]

        teamwork = [
            "Ambil peran yang memanfaatkan preferensi dominan, tapi latih 1 area berlawanan untuk keseimbangan.",
            "Terapkan ritme kerja: planning singkat → eksekusi fokus → review → perbaikan kecil.",
            "Gunakan alat bantu sederhana (notes/checklist/calendar) agar konsisten, terlepas dari tipe Anda.",
            "Bangun kesepakatan tim: cara memberi feedback, prioritas, dan definisi ‘selesai’.",
        ]

        routines = [
            "Refleksi mingguan 10 menit: apa yang efektif, apa pemicunya, dan 1 perbaikan kecil minggu depan.",
            "Latih ‘pause 10 detik’ sebelum merespons situasi emosional: tarik napas → pilih respons paling berguna.",
            "Latih komunikasi tertulis: ringkas (3 poin) + next step yang jelas.",
            "Atur energi sesuai E/I: jadwalkan waktu re-charge (sunyi atau sosial) sebagai bagian produktivitas.",
        ]

        # summary_md: paragraf per-type panjang DI AWAL (paling atas)
        summary = (
            f"**{code} — {name_en}**\n\n"
            f"{type_long[code]}\n\n"
            f"*Tagline:* {tagline}\n\n"
            f"{intro_framework}\n\n"
            "**Interpretasi singkat preferensi Anda:**\n"
            + "\n".join(pref_paras)
            + "\n\n"
            "**Kecenderungan dominansi dimensi (berdasarkan jawaban Anda):**\n"
            + "\n".join([f"- {line}" for line in dim_insights])
        )

        return {
            "title": f"{code} — {name_en}",
            "subtitle": tagline,
            "summary_md": summary,
            "sections": [
                {"title": "Ringkasan Preferensi", "items": dim_insights},
                {"title": "Kekuatan Utama", "items": strengths},
                {"title": "Tantangan Umum", "items": challenges},
                {"title": "Saran Komunikasi", "items": communication},
                {"title": "Saran Karier & Kerja Tim", "items": teamwork},
                {"title": "Rutinitas Pengembangan Diri", "items": routines},
            ],
        }

    # ---------------------------
    # OCEAN
    # ---------------------------
    def _score_ocean(self, answers: Dict[int, int]) -> Dict[str, Any]:
        scores = {k: 0 for k in ["O", "C", "E", "A", "N"]}
        for i, (trait, _) in enumerate(OCEAN_QUESTIONS):
            scores[trait] += int(answers.get(i, 0))

        total = sum(scores.values()) or 1
        percentages = {k: scores[k] / total * 100 for k in scores}

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top1 = sorted_scores[0][0]
        top2 = sorted_scores[1][0]

        # combine if close
        if sorted_scores[0][1] - sorted_scores[1][1] <= 5:
            a, b = sorted([top1, top2])
            result_key = f"{a}_{b}"
        else:
            result_key = top1

        content = self._ocean_content(scores, percentages, result_key)

        return {
            "test_id": "ocean",
            "result_type": result_key,
            "scores": scores,
            "percentages": percentages,
            "chart_kind": "barh",
            "content": content,
        }

    def _ocean_content(self, scores: Dict[str, int], percentages: Dict[str, float], result_key: str) -> Dict[str, Any]:
        trait_names = {
            "O": "Openness (Keterbukaan)",
            "C": "Conscientiousness (Kedisiplinan)",
            "E": "Extraversion (Sosialitas)",
            "A": "Agreeableness (Kooperatif)",
            "N": "Neuroticism (Sensitivitas Stres)",
        }

        # 1 paragraf panjang PER "RESULT TYPE" untuk OCEAN (single + combo)
        profile_long: Dict[str, str] = {
            "O": (
                "Profil Anda menunjukkan Openness sebagai dimensi yang paling dominan. Secara umum, ini berkaitan dengan rasa ingin tahu, "
                "keterbukaan pada ide baru, serta kenyamanan mengeksplorasi kemungkinan. Anda cenderung cepat melihat pola dan peluang, "
                "mudah tertarik pada konsep, dan menikmati variasi dalam belajar maupun bekerja. Dalam konteks pekerjaan, Anda biasanya "
                "unggul pada tugas yang membutuhkan kreativitas, strategi, inovasi, dan pemecahan masalah yang tidak standar. Tantangan "
                "yang mungkin muncul adalah kurangnya ketertarikan pada tugas rutin yang repetitif atau keinginan untuk terus mengeksplorasi "
                "hingga eksekusi tertunda. Pengembangan paling efektif adalah menyeimbangkan eksplorasi dengan sistem eksekusi: buat ide menjadi "
                "eksperimen kecil yang terukur (time-box), lalu evaluasi hasilnya. Dengan begitu, kreativitas Anda menghasilkan dampak nyata."
            ),
            "C": (
                "Profil Anda menunjukkan Conscientiousness sebagai dimensi yang paling dominan. Ini biasanya terkait keteraturan, disiplin, "
                "konsistensi, dan fokus pada penyelesaian. Anda cenderung nyaman dengan rencana, standardisasi, dan definisi ‘done’ yang jelas. "
                "Dalam pekerjaan, Anda sering unggul pada peran yang membutuhkan ketelitian, manajemen waktu, kualitas, dan tanggung jawab "
                "jangka panjang. Tantangan yang dapat muncul adalah perfeksionisme atau kecenderungan over-control—terutama ketika standar Anda "
                "tinggi namun sumber daya terbatas. Pengembangan terbaik adalah mempertahankan kekuatan struktur sambil melatih fleksibilitas: "
                "tentukan standar minimum yang cukup baik, gunakan iterasi, dan sisakan ruang untuk ketidakpastian agar produktivitas tetap stabil."
            ),
            "E": (
                "Profil Anda menunjukkan Extraversion sebagai dimensi yang paling dominan. Secara umum, ini berkaitan dengan energi sosial, "
                "ekspresivitas, dan kenyamanan berinteraksi. Anda cenderung mudah terhubung, cepat memulai komunikasi, dan sering mendapatkan "
                "energi dari kolaborasi. Dalam konteks kerja, Anda biasanya unggul pada peran yang melibatkan koordinasi, presentasi, negosiasi, "
                "atau kolaborasi lintas pihak. Tantangan yang mungkin muncul adalah distraksi karena terlalu banyak interaksi atau diskusi tanpa "
                "output. Pengembangan yang efektif adalah membangun ritme: diskusi singkat yang terstruktur, lalu blok waktu fokus untuk eksekusi. "
                "Dengan cara ini, energi sosial Anda menjadi akselerator hasil, bukan sumber kehilangan fokus."
            ),
            "A": (
                "Profil Anda menunjukkan Agreeableness sebagai dimensi yang paling dominan. Ini berkaitan dengan empati, kerja sama, dan kecenderungan "
                "menjaga harmoni. Anda cenderung mempertimbangkan dampak pada orang lain, mudah membantu, dan kuat dalam membangun kepercayaan. Dalam "
                "tim, Anda sering menjadi penyeimbang yang membuat kerja sama berjalan lebih mulus. Tantangan yang dapat muncul adalah kesulitan "
                "bersikap tegas, menghindari konflik yang sebenarnya perlu diselesaikan, atau terlalu memprioritaskan kebutuhan orang hingga kebutuhan "
                "sendiri tertinggal. Pengembangan terbaik adalah melatih asertif: menyampaikan batasan dan kebutuhan dengan jelas, tanpa kehilangan "
                "kehangatan. Dengan begitu, Anda tetap kooperatif sekaligus efektif dalam pengambilan keputusan."
            ),
            "N": (
                "Profil Anda menunjukkan Neuroticism sebagai dimensi yang paling dominan. Ini berkaitan dengan sensitivitas terhadap stres, kekhawatiran, "
                "dan fluktuasi emosi saat tekanan meningkat. Penting: ini bukan berarti Anda ‘lemah’, melainkan Anda cenderung lebih responsif terhadap "
                "lingkungan—yang bisa menjadi kekuatan jika dikelola, karena meningkatkan kewaspadaan dan ketelitian. Tantangan yang umum adalah mudah "
                "overthinking, cepat lelah emosional, atau memandang situasi dari sisi risiko berlebihan. Pengembangan terbaik adalah strategi coping yang "
                "konsisten: sleep hygiene, time-box untuk berpikir, journaling, serta latihan regulasi emosi (napas, grounding). Saat stabil, Anda bisa "
                "mengubah sensitivitas menjadi ketajaman membaca risiko dengan cara yang lebih sehat dan produktif."
            ),
            # combo (10 kemungkinan)
            "O_C": (
                "Profil Anda menggabungkan Openness dan Conscientiousness sebagai dua dimensi teratas. Ini sering menggambarkan kombinasi yang kuat: "
                "Anda memiliki ide dan kreativitas (O), sekaligus kemampuan menata eksekusi (C). Anda cenderung bisa berpikir inovatif namun tetap "
                "membangun sistem agar ide menjadi hasil. Tantangan yang mungkin muncul adalah standar yang terlalu tinggi (C) yang memperlambat eksperimen (O), "
                "atau sebaliknya, terlalu banyak ide (O) yang membuat struktur (C) terasa terbebani. Kunci optimalnya adalah iterasi terukur: buat prototipe kecil, "
                "tetapkan definisi ‘cukup baik’, lalu perbaiki bertahap."
            ),
            "O_E": (
                "Profil Anda menonjol pada Openness dan Extraversion. Ini sering terlihat pada pribadi yang antusias mengeksplorasi ide sekaligus "
                "nyaman mengekspresikannya melalui diskusi, jejaring, atau kolaborasi. Anda cenderung cepat menangkap peluang, memicu brainstorming, "
                "dan menggerakkan orang dengan energi ide. Tantangan umum adalah fokus—karena ada banyak stimulasi (E) dan banyak kemungkinan (O). "
                "Agar efektif, gunakan aturan sederhana: pilih 1–2 ide prioritas, time-box eksplorasi, lalu buat action item yang konkret."
            ),
            "O_A": (
                "Profil Anda menonjol pada Openness dan Agreeableness. Anda cenderung kreatif dan terbuka pada ide baru, sekaligus peka pada orang lain "
                "dan menjaga harmoni. Kombinasi ini sering menghasilkan gaya kolaborasi yang hangat: Anda bisa mengembangkan gagasan baru tanpa membuat "
                "orang merasa terancam. Tantangan yang bisa muncul adalah terlalu banyak kompromi sehingga ide kehilangan ketegasan, atau menunda keputusan "
                "agar semua nyaman. Kunci optimalnya adalah menjaga empati sambil tetap tegas pada tujuan: sepakati kriteria keputusan dan batas waktu."
            ),
            "O_N": (
                "Profil Anda menonjol pada Openness dan Neuroticism. Anda cenderung memiliki imajinasi dan refleksi yang kuat, sehingga mampu melihat banyak "
                "kemungkinan—termasuk risiko yang mungkin luput dari orang lain. Kombinasi ini dapat menghasilkan kualitas analisis yang tajam, namun juga "
                "berpotensi memicu overthinking jika tidak dikelola. Pengembangan terbaik adalah menyalurkan refleksi menjadi aksi kecil: tulis opsi → pilih satu "
                "langkah pertama → evaluasi. Gunakan time-box untuk berpikir dan praktik regulasi emosi agar kreativitas tidak berubah menjadi kecemasan."
            ),
            "C_E": (
                "Profil Anda menonjol pada Conscientiousness dan Extraversion. Ini sering terlihat pada pribadi yang energik dalam kolaborasi, namun tetap "
                "terstruktur dan berorientasi hasil. Anda cenderung mampu mengorganisir orang, menjaga ritme kerja, dan memastikan target tercapai. Tantangan "
                "yang mungkin muncul adalah kelelahan karena terlalu banyak tanggung jawab dan interaksi sekaligus. Kunci optimalnya adalah delegasi, pembagian "
                "prioritas, dan menjaga jadwal re-charge agar performa tetap stabil."
            ),
            "C_A": (
                "Profil Anda menonjol pada Conscientiousness dan Agreeableness. Anda cenderung dapat diandalkan, rapi, dan juga hangat dalam relasi. Kombinasi "
                "ini sering membuat Anda menjadi ‘penopang’ tim: menjaga kualitas sekaligus menjaga suasana. Tantangan umum adalah sulit berkata tidak, sehingga "
                "tanggung jawab menumpuk. Kunci berkembang adalah batas sehat: tentukan kapasitas, komunikasikan prioritas, dan minta dukungan ketika beban sudah "
                "melewati batas."
            ),
            "C_N": (
                "Profil Anda menonjol pada Conscientiousness dan Neuroticism. Anda cenderung bertanggung jawab, detail-oriented, dan sensitif terhadap tanda-tanda "
                "risiko. Kombinasi ini bisa menghasilkan kualitas kerja yang tinggi, namun rentan memicu perfeksionisme dan kelelahan jika tekanan tidak dikelola. "
                "Kunci optimalnya adalah standar minimum yang jelas (cukup baik), time-box revisi, dan rutinitas pemulihan (tidur, jeda, olahraga ringan). Dengan "
                "strategi ini, ketelitian Anda tetap menjadi kekuatan tanpa menguras energi."
            ),
            "E_A": (
                "Profil Anda menonjol pada Extraversion dan Agreeableness. Anda cenderung ramah, mudah bergaul, dan kooperatif. Kombinasi ini biasanya membuat "
                "Anda kuat dalam membangun jaringan, kerja tim, dan menjaga harmoni. Tantangan umum adalah terlalu banyak menyenangkan orang atau kesulitan bersikap "
                "tegas saat dibutuhkan. Kunci berkembang adalah asertif yang hangat: sampaikan batasan, tetap sopan, dan fokus pada solusi."
            ),
            "E_N": (
                "Profil Anda menonjol pada Extraversion dan Neuroticism. Anda cenderung ekspresif dan responsif, namun juga sensitif terhadap tekanan. Dalam tim, Anda "
                "bisa sangat peduli dan cepat merespons situasi, tetapi bisa mudah lelah jika interaksi dan stres berjalan bersamaan. Pengembangan terbaik adalah manajemen "
                "energi: jadwalkan jeda, batasi overload sosial, gunakan teknik regulasi emosi, dan buat struktur sederhana agar pikiran tidak ‘berlari’ terlalu jauh."
            ),
            "A_N": (
                "Profil Anda menonjol pada Agreeableness dan Neuroticism. Anda cenderung empatik dan peduli, namun juga mudah terpengaruh emosi saat tekanan meningkat. "
                "Kombinasi ini sering membuat Anda peka terhadap kebutuhan orang dan suasana, tetapi berisiko menahan konflik atau menyalahkan diri sendiri. Kunci berkembang "
                "adalah membangun batas sehat, latihan self-compassion, dan komunikasi kebutuhan secara langsung. Dengan coping yang baik, empati Anda menjadi kekuatan yang "
                "stabil, bukan sumber kelelahan."
            ),
        }

        trait_meanings = {
            "O": "Mencerminkan rasa ingin tahu, kreativitas, dan minat pada ide/pengalaman baru.",
            "C": "Mencerminkan keteraturan, disiplin, konsistensi, dan orientasi tujuan.",
            "E": "Mencerminkan kebutuhan stimulasi sosial, energi interaksi, dan ekspresivitas.",
            "A": "Mencerminkan empati, kerja sama, dan kecenderungan menjaga harmoni.",
            "N": "Mencerminkan sensitivitas terhadap stres, kekhawatiran, dan fluktuasi emosi.",
        }

        def level(pct: float) -> str:
            if pct >= 24:
                return "tinggi"
            if pct <= 16:
                return "rendah"
            return "sedang"

        # Long paragraph per result_type (fallback kalau result_key tidak ada)
        long_paragraph = profile_long.get(result_key)
        if not long_paragraph:
            # Generate from top two traits
            top2 = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:2]
            (t1, p1), (t2, p2) = top2
            long_paragraph = (
                f"Profil Anda paling menonjol pada **{trait_names[t1]}** dan **{trait_names[t2]}**. "
                f"Ini berarti kecenderungan Anda banyak dipengaruhi oleh {trait_meanings.get(t1, '')} serta {trait_meanings.get(t2, '')}. "
                "Gunakan laporan ini untuk memahami kapan Anda paling efektif, apa pemicu stres, dan kebiasaan apa yang paling berdampak jika ditingkatkan. "
                "Skor tinggi tidak selalu lebih baik, dan skor rendah tidak selalu buruk—yang penting adalah kecocokan konteks dan keseimbangan strategi."
            )

        intro_framework = (
            "Big Five (OCEAN) bersifat **kontinu**: setiap dimensi berada pada rentang rendah → sedang → tinggi. "
            "Artinya, Anda tidak ‘menjadi satu hal’, melainkan memiliki tingkat kecenderungan tertentu pada masing-masing dimensi. "
            "Gunakan hasil ini sebagai alat refleksi dan pengembangan kebiasaan yang terukur."
        )

        per_trait_lines: List[str] = []
        per_trait_detail: List[str] = []
        for key in ["O", "C", "E", "A", "N"]:
            pct = percentages[key]
            lvl = level(pct)
            per_trait_lines.append(f"{trait_names[key]}: ±{pct:.1f}% ({lvl})")
            per_trait_detail.append(f"**{trait_names[key]} — {lvl}**: {trait_meanings[key]}")

        strengths = [
            "Memberi peta terstruktur untuk memahami gaya kerja, komunikasi, dan respons terhadap tekanan.",
            "Membantu menyusun strategi pengembangan diri berbasis dimensi spesifik (mis. disiplin, adaptasi, empati).",
            "Membuat refleksi lebih terukur: Anda bisa fokus pada kebiasaan yang paling berdampak.",
        ]

        development: List[str] = []
        for t, pct in sorted(percentages.items(), key=lambda x: x[1], reverse=True):
            nm = trait_names[t]
            lvl = level(pct)
            if lvl == "tinggi":
                development.append(
                    f"**{nm} tinggi**: manfaatkan sebagai kekuatan, tetapi jaga keseimbangan agar tidak ‘overdoing’."
                )
            elif lvl == "rendah":
                development.append(
                    f"**{nm} rendah**: jadikan fokus latihan bertahap lewat kebiasaan kecil dan konsisten."
                )

        routines = [
            "Pilih 1 dimensi untuk dilatih selama 14 hari (contoh: C → checklist harian 3 tugas).",
            "Journaling 5 menit: pemicu → respons → alternatif respons (terutama untuk N).",
            "Time-box fokus: 25–50 menit kerja fokus + jeda 5–10 menit.",
            "Refleksi mingguan: 1 hal berhasil, 1 hal perlu perbaikan, 1 aksi kecil berikutnya.",
        ]

        summary = (
            f"**Big Five (OCEAN)**\n\n"
            f"{long_paragraph}\n\n"
            f"{intro_framework}\n\n"
            f"**Ringkasan profil (key): {result_key}**"
        )

        return {
            "title": "Big Five (OCEAN)",
            "subtitle": f"Ringkasan profil: {result_key}",
            "summary_md": summary,
            "sections": [
                {"title": "Skor Dimensi", "items": per_trait_lines},
                {"title": "Penjelasan Tiap Dimensi (Detail)", "items": per_trait_detail},
                {"title": "Kekuatan & Manfaat", "items": strengths},
                {"title": "Saran Pengembangan (Berdasarkan Skor)", "items": development},
                {"title": "Rutinitas Praktis", "items": routines},
            ],
        }

    # ---------------------------
    # Enneagram
    # ---------------------------
    def _score_enneagram(self, answers: Dict[int, int]) -> Dict[str, Any]:
        scores = {str(k): 0 for k in range(1, 10)}
        for i, (etype, _) in enumerate(ENNEAGRAM_QUESTIONS):
            scores[str(etype)] += int(answers.get(i, 0))

        result = max(scores, key=scores.get)
        total = sum(scores.values()) or 1
        percentages = {k: (v / total * 100) for k, v in scores.items()}

        content = self._enneagram_content(result)

        return {
            "test_id": "enneagram",
            "result_type": result,
            "scores": scores,
            "percentages": percentages,
            "chart_kind": "barh",
            "content": content,
        }

    def _enneagram_content(self, t: str) -> Dict[str, Any]:
        names = {
            "1": "The Reformer",
            "2": "The Helper",
            "3": "The Achiever",
            "4": "The Individualist",
            "5": "The Investigator",
            "6": "The Loyalist",
            "7": "The Enthusiast",
            "8": "The Challenger",
            "9": "The Peacemaker",
        }

        short = {
            "1": "Berorientasi prinsip, integritas, dan standar kualitas.",
            "2": "Hangat, suportif, dan termotivasi untuk membantu.",
            "3": "Berorientasi prestasi, citra, dan efektivitas.",
            "4": "Autentik, ekspresif, dan peka pada identitas.",
            "5": "Analitis, observatif, dan menghargai pengetahuan.",
            "6": "Loyal, waspada, dan butuh rasa aman.",
            "7": "Optimis, spontan, dan pencari pengalaman baru.",
            "8": "Tegas, protektif, dan menyukai kontrol.",
            "9": "Tenang, damai, dan mediator yang baik.",
        }

        # 1 paragraf panjang PER TYPE Enneagram
        enneagram_long: Dict[str, str] = {
            "1": (
                "Sebagai Enneagram Type 1, Anda cenderung berorientasi pada integritas, standar, dan keinginan untuk melakukan hal yang benar. "
                "Anda biasanya peka terhadap ketidakteraturan dan memiliki dorongan kuat untuk memperbaiki kualitas—baik pada diri sendiri maupun lingkungan. "
                "Dalam konteks kerja, Anda sering unggul karena disiplin, ketelitian, dan komitmen pada hasil yang rapi. Tantangan yang umum adalah "
                "perfeksionisme, kritik berlebih (pada diri sendiri atau orang lain), dan kesulitan menerima bahwa ‘cukup baik’ kadang sudah memadai. "
                "Saat stres, Anda bisa menjadi kaku atau mudah frustrasi. Pengembangan terbaik untuk Type 1 adalah melatih self-compassion, membedakan "
                "standar sehat vs kontrol berlebihan, serta membangun kebiasaan relaksasi agar energi tidak habis untuk mengejar kesempurnaan."
            ),
            "2": (
                "Sebagai Enneagram Type 2, Anda cenderung hangat, suportif, dan termotivasi untuk membantu serta merasa dibutuhkan. Anda biasanya cepat "
                "membaca kebutuhan orang, membangun relasi, dan menciptakan rasa aman secara emosional. Dalam tim, Anda sering menjadi perekat sosial yang "
                "membuat orang merasa diperhatikan. Tantangan yang umum adalah sulit berkata tidak, memberi berlebihan hingga lelah, atau diam-diam berharap "
                "balasan yang sepadan. Saat stres, Anda bisa menjadi sensitif atau merasa tidak dihargai. Kunci berkembang bagi Type 2 adalah batas sehat, "
                "belajar meminta bantuan, dan memvalidasi diri tanpa bergantung pada approval orang lain."
            ),
            "3": (
                "Sebagai Enneagram Type 3, Anda cenderung berorientasi pada pencapaian, efektivitas, dan hasil. Anda biasanya adaptif, cepat menangkap "
                "ekspektasi, dan mampu menggerakkan diri untuk mencapai target. Dalam pekerjaan, Type 3 sering unggul karena produktif dan fokus outcome. "
                "Tantangan yang umum adalah overwork, terlalu mengandalkan citra, atau mengabaikan kebutuhan emosional karena sibuk ‘harus berhasil’. Saat stres, "
                "Anda bisa makin memaksa diri atau sulit mengakui keterbatasan. Pengembangan terbaik untuk Type 3 adalah mendefinisikan sukses versi diri, menjaga "
                "ritme recovery, dan membangun kehadiran (mindfulness) agar identitas tidak hanya melekat pada prestasi."
            ),
            "4": (
                "Sebagai Enneagram Type 4, Anda cenderung peka, autentik, dan berorientasi pada identitas serta makna personal. Anda biasanya memiliki kedalaman "
                "emosi dan kepekaan estetika/ekspresi diri. Dalam konteks kreatif atau peran yang membutuhkan empati, Type 4 sering sangat kuat. Tantangan yang umum "
                "adalah mood swing, membandingkan diri, atau terjebak pada perasaan ‘kurang’ sehingga sulit bergerak. Saat stres, Anda bisa overthinking atau menarik "
                "diri. Kunci berkembang bagi Type 4 adalah rutinitas stabil, memisahkan fakta vs interpretasi, dan fokus aksi kecil konsisten agar emosi menjadi sumber "
                "kekuatan, bukan penghambat."
            ),
            "5": (
                "Sebagai Enneagram Type 5, Anda cenderung analitis, observatif, dan menghargai pengetahuan serta kompetensi. Anda biasanya nyaman memahami hal secara "
                "mendalam, memetakan sistem, dan menghemat energi dengan memilih interaksi yang selektif. Dalam pekerjaan, Anda sering unggul pada riset, analisis, "
                "problem-solving, dan desain konsep. Tantangan yang umum adalah menarik diri terlalu jauh, menunda tindakan karena ingin paham sempurna, atau tampak "
                "dingin secara emosional. Saat stres, Anda bisa makin mengisolasi diri. Pengembangan terbaik bagi Type 5 adalah menyeimbangkan teori dan praktik: "
                "membuat eksperimen kecil, membangun keterlibatan sosial bertahap, dan menyederhanakan komunikasi agar insight Anda lebih mudah diakses orang lain."
            ),
            "6": (
                "Sebagai Enneagram Type 6, Anda cenderung loyal, waspada, dan berorientasi pada keamanan serta kepastian. Anda biasanya pandai mengantisipasi risiko, "
                "membuat rencana, dan menjaga tanggung jawab. Dalam tim, Type 6 sering menjadi ‘penjaga sistem’ yang memastikan hal-hal tidak jatuh berantakan. Tantangan "
                "yang umum adalah cemas, ragu, atau terlalu banyak skenario ‘what if’ sehingga keputusan tertunda. Saat stres, Anda bisa overprepare atau sulit percaya. "
                "Pengembangan terbaik bagi Type 6 adalah menguji asumsi dengan data, membuat rencana A/B yang sederhana, dan melatih keberanian mencoba melalui keputusan kecil "
                "yang konsisten."
            ),
            "7": (
                "Sebagai Enneagram Type 7, Anda cenderung optimis, spontan, dan mencari pengalaman baru. Anda biasanya energik, cepat melihat peluang, dan menikmati variasi. "
                "Dalam pekerjaan, Type 7 sering unggul pada ideasi, networking, dan memicu semangat tim. Tantangan yang umum adalah impulsif, kurang fokus, atau menghindari "
                "ketidaknyamanan sehingga sulit menyelesaikan hal yang monoton. Saat stres, Anda bisa makin distraktif. Kunci berkembang bagi Type 7 adalah melatih fokus 1 hal, "
                "membangun toleransi pada bosan/ketidaknyamanan, dan menyelesaikan sebelum pindah agar energi Anda menghasilkan output yang nyata."
            ),
            "8": (
                "Sebagai Enneagram Type 8, Anda cenderung tegas, protektif, dan berorientasi kontrol atas hidup Anda. Anda biasanya berani, cepat mengambil keputusan, dan "
                "mampu memimpin dalam situasi sulit. Dalam tim, Type 8 sering menjadi pendorong aksi dan pelindung. Tantangan yang umum adalah terlihat terlalu dominan, keras, "
                "atau sulit menunjukkan kerentanan. Saat stres, Anda bisa makin konfrontatif atau menekan. Pengembangan terbaik bagi Type 8 adalah melatih empati saat konflik, "
                "mendengar sebelum merespons, dan membangun kepercayaan lewat delegasi agar kekuatan Anda terasa aman bagi orang lain."
            ),
            "9": (
                "Sebagai Enneagram Type 9, Anda cenderung tenang, damai, dan menjaga harmoni. Anda biasanya mampu menengahi, mendengarkan, dan membuat suasana lebih stabil. "
                "Dalam tim, Type 9 sering menjadi penyeimbang konflik dan membantu kolaborasi berjalan mulus. Tantangan yang umum adalah menunda, menghindari konflik, atau "
                "mengabaikan kebutuhan sendiri demi kenyamanan semua orang. Saat stres, Anda bisa semakin pasif. Kunci berkembang bagi Type 9 adalah time-box untuk mulai, "
                "menentukan prioritas harian, dan berlatih konflik sehat (mengatakan kebutuhan) agar Anda tetap hadir dan berpengaruh."
            ),
        }

        core = {
            "1": ("Integritas & kebenaran", "Takut melakukan kesalahan/menjadi ‘buruk’", "Menjadi baik, benar, dan bermakna"),
            "2": ("Diterima & dibutuhkan", "Takut tidak dicintai/diabaikan", "Dicintai karena memberi"),
            "3": ("Sukses & nilai diri", "Takut gagal/tidak bernilai", "Diakui lewat pencapaian"),
            "4": ("Identitas & keunikan", "Takut tidak punya jati diri/arti", "Menemukan makna personal"),
            "5": ("Pemahaman & kompetensi", "Takut tidak mampu/terkuras", "Menguasai pengetahuan & mandiri"),
            "6": ("Keamanan & kepastian", "Takut tanpa dukungan/terancam", "Merasa aman & siap menghadapi risiko"),
            "7": ("Kebebasan & pengalaman", "Takut terjebak sakit/terbatas", "Menikmati hidup & pilihan luas"),
            "8": ("Kontrol & perlindungan", "Takut dikendalikan/dirugikan", "Berdaulat & melindungi"),
            "9": ("Damai & stabil", "Takut konflik/kehilangan koneksi", "Harmoni & ketenangan"),
        }

        strengths_map = {
            "1": ["Berintegritas", "Disiplin", "Dapat diandalkan", "Menjaga kualitas"],
            "2": ["Empatik", "Dermawan", "Membangun relasi", "Membaca kebutuhan orang"],
            "3": ["Produktif", "Adaptif", "Berorientasi tujuan", "Mendorong performa"],
            "4": ["Kreatif", "Peka emosi", "Autentik", "Berani mengekspresikan diri"],
            "5": ["Analitis", "Mandiri", "Objektif", "Mendalam dalam berpikir"],
            "6": ["Loyal", "Perencana", "Tanggung jawab", "Mampu mengantisipasi risiko"],
            "7": ["Optimis", "Inovatif", "Energik", "Mudah melihat peluang"],
            "8": ["Berani", "Tegas", "Melindungi", "Mampu memimpin saat krisis"],
            "9": ["Menengahi", "Sabar", "Stabil", "Menenangkan suasana"],
        }

        challenges_map = {
            "1": ["Perfeksionis", "Kritis", "Kaku", "Sulit puas"],
            "2": ["Sulit berkata tidak", "Terlalu mengutamakan orang", "Rentan kecewa", "Butuh validasi"],
            "3": ["Overwork", "Terlalu fokus citra", "Mengabaikan emosi", "Takut terlihat lemah"],
            "4": ["Mood swing", "Membandingkan diri", "Overthinking", "Terlalu fokus ‘yang kurang’"],
            "5": ["Menarik diri", "Kaku emosional", "Overanalyze", "Menunda tindakan"],
            "6": ["Cemas", "Ragu", "Overprepare", "Menguji kepercayaan orang"],
            "7": ["Menghindari ketidaknyamanan", "Kurang fokus", "Impulsif", "Sulit menyelesaikan"],
            "8": ["Dominan", "Keras", "Sulit rentan", "Cepat konfrontasi"],
            "9": ["Menunda", "Menghindari konflik", "Sulit prioritas", "Mengecilkan kebutuhan diri"],
        }

        growth = {
            "1": ["Latih self-compassion", "Bedakan standar vs kontrol", "Latihan ‘cukup baik’"],
            "2": ["Tetapkan batas sehat", "Minta bantuan", "Validasi diri tanpa approval"],
            "3": ["Definisikan sukses versi diri", "Jadwalkan recovery", "Latih mindfulness"],
            "4": ["Rutinitas stabil", "Pisahkan fakta vs interpretasi", "Aksi kecil konsisten"],
            "5": ["Seimbangkan teori & praktik", "Keterlibatan sosial bertahap", "Komunikasi sederhana"],
            "6": ["Uji asumsi lewat data", "Rencana A/B sederhana", "Keputusan kecil konsisten"],
            "7": ["Fokus 1 hal", "Toleransi bosan", "Selesaikan sebelum pindah"],
            "8": ["Dengar sebelum respons", "Latih empati", "Delegasi & percaya"],
            "9": ["Time-box mulai", "Prioritas harian", "Latih konflik sehat"],
        }

        focus, fear, desire = core.get(t, ("", "", ""))
        long_paragraph = enneagram_long.get(t, "")

        summary = (
            f"**Enneagram Type {t} — {names.get(t, '')}**\n\n"
            f"{long_paragraph}\n\n"
            f"*Ringkas:* {short.get(t, '')}\n\n"
            f"**Motivasi inti:** {focus}\n"
            f"**Ketakutan inti:** {fear}\n"
            f"**Keinginan inti:** {desire}\n\n"
            "Enneagram berfokus pada motivasi (mengapa Anda bertindak). Gunakan hasil ini sebagai bahan refleksi dan latihan kebiasaan."
        )

        return {
            "title": f"Enneagram Type {t} — {names.get(t, '')}",
            "subtitle": short.get(t, ""),
            "summary_md": summary,
            "sections": [
                {"title": "Kekuatan Utama", "items": strengths_map.get(t, [])},
                {"title": "Tantangan Umum", "items": challenges_map.get(t, [])},
                {"title": "Saran Pengembangan", "items": growth.get(t, [])},
            ],
        }

    # ---------------------------
    # Temperament
    # ---------------------------
    def _score_temperament(self, answers: Dict[int, int]) -> Dict[str, Any]:
        scores = {k: 0 for k in ["S", "C", "P", "M"]}
        for i, (trait, _) in enumerate(TEMPERAMENT_QUESTIONS):
            scores[trait] += int(answers.get(i, 0))

        result = max(scores, key=scores.get)
        total = sum(scores.values()) or 1
        percentages = {k: (v / total * 100) for k, v in scores.items()}

        content = self._temperament_content(result)

        return {
            "test_id": "temperament",
            "result_type": result,
            "scores": scores,
            "percentages": percentages,
            "chart_kind": "barh",
            "content": content,
        }

    def _temperament_content(self, t: str) -> Dict[str, Any]:
        names = {"S": "Sanguine", "C": "Choleric", "P": "Phlegmatic", "M": "Melancholic"}
        desc = {
            "S": "Antusias, ekspresif, dan mudah membangun koneksi sosial.",
            "C": "Tegas, fokus tujuan, percaya diri, dan berorientasi hasil.",
            "P": "Tenang, kooperatif, dan menjaga harmoni.",
            "M": "Teliti, terstruktur, dan peka terhadap kualitas serta detail.",
        }

        # 1 paragraf panjang PER Temperament
        temp_long: Dict[str, str] = {
            "S": (
                "Sebagai Sanguine, Anda cenderung antusias, ekspresif, dan mudah membangun suasana yang hidup. Anda biasanya cepat "
                "membuat koneksi sosial, membawa energi positif, dan nyaman berinteraksi. Dalam pekerjaan atau organisasi, Sanguine "
                "sering unggul pada peran yang melibatkan komunikasi, presentasi, event, komunitas, atau kolaborasi lintas orang. Tantangan "
                "yang umum adalah konsistensi—karena Anda mudah terdistraksi oleh hal baru atau suasana yang berubah. Saat tertekan, Anda "
                "bisa mencari distraksi daripada menyelesaikan akar masalah. Pengembangan terbaik adalah struktur ringan: 3 prioritas harian, "
                "time-box fokus, dan kebiasaan review singkat agar energi Anda menghasilkan output yang stabil."
            ),
            "C": (
                "Sebagai Choleric, Anda cenderung tegas, cepat, dan berorientasi hasil. Anda biasanya nyaman memimpin, mengambil keputusan, "
                "dan mendorong eksekusi saat situasi membutuhkan arah yang jelas. Dalam tim, Anda sering menjadi motor penggerak yang memastikan "
                "target tercapai. Tantangan yang umum adalah kesabaran dan gaya komunikasi: saat tekanan meningkat, Anda bisa terdengar keras atau "
                "terlalu menekan. Pengembangan terbaik adalah menyeimbangkan ketegasan dengan empati: jelaskan tujuan, dengarkan kebutuhan tim, dan "
                "latih jeda sebelum merespons konflik. Dengan begitu, kekuatan Anda terasa aman sekaligus efektif."
            ),
            "P": (
                "Sebagai Phlegmatic, Anda cenderung tenang, stabil, dan menjaga harmoni. Anda biasanya pendengar yang baik, kooperatif, serta "
                "mampu menengahi konflik agar suasana tetap kondusif. Dalam tim, Anda sering menjadi penyeimbang yang membuat kolaborasi berjalan mulus. "
                "Tantangan yang umum adalah menunda keputusan, menghindari konflik, atau kurang asertif dalam menyampaikan kebutuhan. Saat tertekan, Anda "
                "bisa semakin pasif dan memilih diam. Pengembangan terbaik adalah membangun keberanian bertahap: time-box untuk mulai, prioritas harian, "
                "dan latihan komunikasi kebutuhan secara langsung agar Anda tetap hadir dan berpengaruh."
            ),
            "M": (
                "Sebagai Melancholic, Anda cenderung teliti, terstruktur, dan berorientasi kualitas. Anda biasanya kuat dalam analisis, detail, dan "
                "konsistensi proses. Dalam pekerjaan, Anda sering unggul pada peran yang membutuhkan perencanaan, dokumentasi, quality assurance, dan "
                "pemikiran sistematis. Tantangan yang umum adalah perfeksionisme dan overthinking—terutama saat standar tinggi bertemu keterbatasan waktu. "
                "Saat tertekan, Anda bisa cemas dan sulit melepas kontrol. Pengembangan terbaik adalah mendefinisikan ‘cukup baik’, membatasi revisi dengan time-box, "
                "serta menjaga ritme istirahat agar kualitas tetap tinggi tanpa mengorbankan kesehatan."
            ),
        }

        strengths = {
            "S": ["Membangun suasana positif", "Komunikatif", "Cepat beradaptasi", "Mudah memotivasi orang"],
            "C": ["Pemimpin alami", "Cepat mengambil keputusan", "Tangguh di bawah tekanan", "Berani menghadapi tantangan"],
            "P": ["Sabar", "Mediator", "Stabil", "Kooperatif dan suportif"],
            "M": ["Detail-oriented", "Analitis", "Berstandar tinggi", "Konsisten dan rapi"],
        }
        challenges = {
            "S": ["Mudah terdistraksi", "Kurang konsisten", "Impulsif", "Kadang melewatkan detail"],
            "C": ["Terlalu dominan", "Kurang sabar", "Terkesan keras", "Sulit kompromi saat tertekan"],
            "P": ["Menunda", "Menghindari konflik", "Kurang asertif", "Sulit memulai keputusan besar"],
            "M": ["Perfeksionis", "Overthinking", "Rentan cemas", "Sulit melepas kontrol kualitas"],
        }
        growth = {
            "S": ["3 prioritas harian", "Time-box fokus", "Latih follow-through", "Review mingguan"],
            "C": ["Latih empati", "Delegasi", "Jeda sebelum merespons", "Libatkan tim dalam solusi"],
            "P": ["Prioritas harian", "Latih berkata tidak", "Time-box mulai", "Latih konflik sehat"],
            "M": ["Definisikan cukup baik", "Batasi revisi", "Pisahkan fakta vs asumsi", "Jaga ritme istirahat"],
        }

        summary = (
            f"**{names.get(t, t)}**\n\n"
            f"{temp_long.get(t, '')}\n\n"
            f"*Ringkas:* {desc.get(t, '')}\n\n"
            "Temperament adalah peta gaya energi dan interaksi. Gunakan hasil ini untuk memahami pola default Anda dan menyiapkan strategi "
            "agar kekuatan bekerja optimal tanpa jatuh ke pola ekstrem saat tertekan."
        )

        return {
            "title": f"{names.get(t, t)}",
            "subtitle": desc.get(t, ""),
            "summary_md": summary,
            "sections": [
                {"title": "Kekuatan", "items": strengths.get(t, [])},
                {"title": "Tantangan", "items": challenges.get(t, [])},
                {"title": "Saran Pengembangan", "items": growth.get(t, [])},
            ],
        }
