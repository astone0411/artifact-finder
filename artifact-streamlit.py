import streamlit as st
import gzip
import io
import pandas as pd

# ======================= CONFIGURE HERE =======================
TARGETS = [
    ("PIK3CA p.E545A", "3", 179218304, "A", "C"),
    ("XRCC5 p.E287fs", "2", 216127588, "TA", "T"),
    ("KMT2C p.C1051*", "7", 152224440, "G", "T"),
    ("ZFHX3 p.A783fs", "16", 72957797, "TGC", "T"),
    ("EP300 p.M1470fs", "22", 41170520, "CA", "C"),
    ("JAK1 p.K860fs", "1", 64841313, "GT", "G"),
    ("FANCD2 p.F162fs", "3", 10036327, "AT", "A"),
    ("ASXL1 p.G646fs", "20", 32434638, "A", "AG"),
    ("BLM p.N515fs", "15", 90760909, "A", "AA"),
    ("DNMT3A p.Q249*", "2", 25248147, "G", "A"),
    ("CHEK2 p.F475fs", "22", 28694067, "TA", "T"),
    ("MRE11 p.N511fs", "11", 94456306, "AT", "A"),
    ("KMT2C p.R904*", "7", 152235876, "G", "A"),
    ("KMT2A p.D877fs", "11", 118473778, "TAG", "T"),
    ("MLH3 p.E586fs", "14", 75047901, "T", "TT"),
    ("MSH6 p.F1088fs", "2", 47803501, "C", "CC"),
    ("B2M p.Q109*", "15", 44715680, "C", "T"),
    ("SETD2 p.Q2285*", "3", 47056931, "G", "A"),
    ("MAP3K1 p.A2fs", "5", 56815575, "TG", "T"),
    ("KMT2C p.C391*", "7", 152265049, "G", "T"),
    ("KMT2C p.M940fs", "7", 152230273, "T", "TA"),
    ("PMS1 p.K164fs", "2", 189818083, "CA", "C"),
    ("FLCN p.H429fs", "17", 17216394, "TG", "T"),
    ("ARID1B p.A423fs", "6", 156778945, "TGGCG", "T"),
    ("ARID1B p.A427fs", "6", 156778956, "GC", "G"),
    ("ARID1B p.A427fs", "6", 156778957, "CCG", "C"),
    ("KMT2C p.C1103*", "7", 152224029, "A", "T"),
    ("EP300 p.R1645*", "22", 41176400, "C", "T"),
    ("ASXL1 p.G645fs", "20", 32434638, "AG", "A"),
    ("ATRX p.R840fs", "X", 77682737, "CT", "C"),
    ("ATRX p.E1461fs", "X", 77652291, "TT", "T"),
    ("PARP1 p.S507fs", "1", 226379945, "CT", "C"),
    ("KMT2D p.P1003fs", "12", 49050579, "TG", "T"),
    ("EP300 p.Q2375*", "22", 41178834, "C", "T"),
    ("EP300 p.Q259*", "22", 41125909, "C", "T"),
    ("KMT2A p.P773fs", "11", 118473470, "AC", "A"),
    ("ATRX p.R1302fs", "X", 77664683, "CT", "C"),
    ("MSH2 p.Q314*", "2", 47414416, "C", "T"),
    ("ATM p.Q368*", "11", 108248969, "C", "T"),
    ("CIC c.4459+2T>G", "19", 42294737, "T", "G"),
    ("PTEN p.A137fs", "10", 87933164, "ATG", "A"),
    ("MRE11 p.R572*", "11", 94447288, "G", "A"),
    ("PRKDC p.K165fs", "8", 47954349, "ATT", "A"),
    ("CHEK1 p.T226fs", "11", 125635482, "G", "GA"),
    ("CIC c.4459+2T>C", "19", 42294737, "T", "C"),
    ("TP53BP1 p.Q411*", "15", 43470016, "G", "A"),
    ("TP53BP1 p.Q19*", "15", 43492421, "G", "A"),
    ("SDHA p.L74fs", "5", 224428, "C", "CT"),
    ("KMT2D p.Q2514*", "12", 49040230, "G", "A"),
    ("RPA1 p.Q524*", "17", 1891851, "C", "T"),
    ("TGFBR2 p.K128fs", "3", 30650379, "GAA", "G"),
    ("ARID1B p.Q871*", "6", 157133057, "C", "T"),
    ("NSD1 p.Q1839*", "5", 177273677, "C", "T"),
    ("BRCA2 p.Q1129*", "13", 32337740, "C", "T"),
    ("RAD51 p.Q268*", "15", 40729880, "C", "T"),
    ("AXIN1 p.Q269*", "16", 346221, "G", "A"),
    ("ARID1B p.Q902*", "6", 157133150, "C", "T"),
    ("ATRX p.Q1877*", "X", 77600502, "G", "A"),
    ("EP300 p.Q1949*", "22", 41177556, "C", "T"),
    ("GRIN2A p.S1341fs", "16", 9763522, "CT", "C"),
    ("MED12 p.S505*", "X", 71123123, "C", "G"),
    ("FLCN p.H429fs", "17", 17216394, "T", "TG"),
    ("KMT2C p.C302*", "7", 152273811, "A", "T"),
    ("KMT2C p.Y306*", "7", 152273799, "A", "C"),
    ("MAP3K1 p.S12*", "5", 56815608, "C", "A"),
    ("KMT2A p.L1660*", "11", 118491912, "T", "A"),
    ("ARID1B p.A540fs", "6", 156779297, "GGC", "G"),
    ("CDK12 p.A408fs", "17", 39471053, "AG", "A"),
    ("MEN1 p.S512*", "11", 64804632, "G", "C"),
    ("ARID1A p.Y803*", "1", 26762309, "T", "A"),
    ("SDHA p.K541*", "5", 251061, "A", "T"),
    ("FANCD2 p.Q1053*", "3", 10081397, "C", "T"),
    ("CIC p.Q378*", "19", 42272915, "C", "T"),
    ("RAD50 p.Q298*", "5", 132587930, "C", "T"),
    ("AXIN1 p.E87*", "16", 346767, "C", "A"),
    ("MSH6 p.C1098*", "2", 47803541, "C", "A"),
    ("KMT2A p.Y1576fs", "11", 118491225, "TA", "T"),
    ("BRIP1 p.Q258*", "17", 61808613, "G", "A"),
    ("MSH2 p.Q130*", "2", 47410115, "C", "T"),
    ("MSH3 p.Q664*", "5", 80768026, "C", "T"),
    ("KMT2A p.Q1804*", "11", 118495755, "C", "T"),
    ("ARID1B p.Q716*", "6", 156901496, "C", "T"),
    ("NBN p.Q644*", "8", 89946280, "G", "A"),
    ("ERCC2 c.1119-2A>C", "19", 45361644, "T", "G"),
    ("BARD1 p.Q253*", "2", 214781117, "G", "A"),
    ("RAD50 p.Q986*", "5", 132609316, "C", "T"),
    ("KMT2C p.Q4739*", "7", 152144841, "G", "A"),
    ("KDM6A p.Q154*", "X", 45020626, "C", "T"),
    ("NBN p.R466fs", "8", 89955283, "CT", "C"),
    ("BLM p.Q1262*", "15", 90809169, "C", "T"),
    ("CREBBP p.I1084fs", "16", 3767719, "CT", "C"),
    ("SMARCA4 p.Q66*", "19", 10984347, "C", "T"),
    ("CEBPA p.D105fs", "19", 33302101, "TCG", "T"),
    ("RAD51C p.Q344*", "17", 58734121, "C", "T"),
    ("FANCF p.Q290*", "11", 22624943, "G", "A"),
    ("GRIN2A p.Q1278*", "16", 9763712, "G", "A"),
    ("ARID1B p.Q1569*", "6", 157200930, "C", "T"),
    ("AR p.Q80del", "X", 67545316, "TGCA", "T"),
    ("ARID1A p.D1850fs", "1", 26779439, "T", "TG"),
    ("ARID1A p.Q546fs", "1", 26731432, "AC", "A"),
    ("ATM p.G2063fs", "11", 108316101, "AG", "A"),
    ("ATR p.I774fs", "3", 142555897, "AT", "A"),
    ("ATR p.I774fs", "3", 142555897, "A", "AT"),
    ("ATR p.I170fs", "3", 142556089, "AT", "A"),
    ("ATR p.I170fs", "3", 142556089, "A", "AT"),
    ("BRCA2 p.T3033fs", "13", 32379885, "CA", "C"),
    ("BRCA2 p.I605fs", "13", 32333283, "GA", "G"),
    ("CCND3 p.259A", "6", 41936044, "A", "C"),
    ("KMT2C c.3323+1G>A", "7", 152224014, "C", "T"),
    ("MED12 c.2422+2T>G", "X", 71125715, "T", "G"),
    ("POLE p.V1148fs", "12", 132643512, "CCA", "C"),
    ("POLE p.S1419fs", "12", 132643869, "CTG", "C"),
    ("RET p.C630G", "10", 43114488, "T", "G"),
    ("SDHA c.64-2A>G", "5", 223480, "A", "G"),
]
# =============================================================


def normalize_chrom(ch):
    ch = str(ch).strip()
    if ch.lower().startswith("chr"):
        ch = ch[3:]
    if ch.upper() in ("M", "MT"):
        return "MT"
    return ch


def parse_targets(targets):
    labels = [t[0] for t in targets]
    targets_by_key = {}

    for label, chrom, pos, ref, alt in targets:
        key = (normalize_chrom(chrom), int(pos))
        if key not in targets_by_key:
            targets_by_key[key] = {}
        targets_by_key[key][label] = (ref, alt)

    return labels, targets_by_key


def scan_vcf(file, targets_by_key):
    # Initialize results
    results = {
        label: False
        for key in targets_by_key
        for label in targets_by_key[key]
    }

    # ✅ Fix: convert binary → text stream
    if file.name.endswith(".gz"):
        reader = io.TextIOWrapper(gzip.GzipFile(fileobj=file))
    else:
        reader = io.TextIOWrapper(file)

    for line in reader:
        if line.startswith("#"):
            continue

        parts = line.strip().split("\t")
        if len(parts) < 5:
            continue

        chrom = normalize_chrom(parts[0])
        pos = int(parts[1])
        ref = parts[3]
        alts = parts[4].split(",")

        key = (chrom, pos)

        if key in targets_by_key:
            for label, (t_ref, t_alt) in targets_by_key[key].items():
                if t_ref is None:
                    results[label] = True
                else:
                    if ref == t_ref and t_alt in alts:
                        results[label] = True

    return results


# ======================= STREAMLIT UI =======================

st.title("🧬 VCF Artifact Scanner 🧬")

uploaded_file = st.file_uploader(
    "Upload a VCF file (.vcf or .vcf.gz)",
    type=["vcf", "gz"]
)

if uploaded_file:
    # Reset pointer in case Streamlit re-runs
    uploaded_file.seek(0)

    labels, targets_by_key = parse_targets(TARGETS)

    with st.spinner("Scanning VCF..."):
        results = scan_vcf(uploaded_file, targets_by_key)

    # Convert results to DataFrame
    df = pd.DataFrame({
        "Artifact": list(results.keys()),
        "Found": list(results.values())
    })

    found_count = int(df["Found"].sum())

    # ✅ Summary
    st.subheader(f"✅ Artifacts Found: {found_count} / {len(df)}")

    # ✅ Full table
    st.dataframe(df, width='stretch')

    # ✅ Filtered results
    st.subheader("Detected Artifacts Only")
    st.dataframe(df[df["Found"]], width='stretch')

    # ✅ Download button
    csv = df.to_csv(index=False)
    st.download_button("Download Results CSV", csv, "artifact_results.csv")