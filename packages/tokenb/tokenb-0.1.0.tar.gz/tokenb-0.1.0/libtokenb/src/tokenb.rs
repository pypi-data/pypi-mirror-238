use aho_corasick::AhoCorasick;
use macro_rules_attribute::macro_rules_attribute;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use tokenizers::{
    impl_serde_type,
    tokenizer::{AddedToken, Result},
    Decoder, NormalizedString, PostProcessor,
};
use tokenizers::{PreTokenizedString, PreTokenizer};

lazy_static::lazy_static! {
    pub static ref DEFAULT_STOKENS: Vec<AddedToken> = DEFAULT_STOKENS_STR
        .iter()
        .map(|&s| AddedToken::from(String::from(s), true))
        .collect();

    pub static ref DEFAULT_STOKENS_FINDS: Vec<&'static str> = DEFAULT_STOKENS_REPLACES.iter().map(|&(_x,y)| y).collect();
    pub static ref DEFAULT_STOKENS_MAP: BTreeMap<String, &'static str> = DEFAULT_STOKENS_REPLACES.iter().map(|&(x,y)| (x.to_string(),y)).collect();
    pub static ref DEFAULT_STOKENS_MAP_REV: BTreeMap<String, &'static str> = DEFAULT_STOKENS_REPLACES.iter().map(|&(x,y)| (y.to_string(),x)).collect();
}

pub const DEFAULT_STOKENS_STR: [&str; 306] = [
    "E", // "<|end|>"
    "P", // "<|padding|>"
    "I", // "<|input|>"
    "G", // "<|ego|>"
    "M", // "<|me|>"
    "A", // "<|mask|>"
    "Q", // "<|question|>"
    "F", // "<|find|>"
    "R", // "<|search|>"
    "T", // "<|think|>"
    "U", // "<|run|>":
    "X", // "<|execute|>":
    "K", // "<|knowledge|>":
    "N", // "<|sentiment|>":
    "Y", // "<|summary|>":
    "O", // "<|goal|>":
    "D", // "<|todo|>":
    "V", // "<|speak|>":
    "W", // "<|write|>":
    "B", // "<|remember|>":
    "Z", // "<|save|>":
    "<|unused22|>",
    "<|unused23|>",
    "<|unused24|>",
    "<|unused25|>",
    "<|unused26|>",
    "<|unused27|>",
    "<|unused28|>",
    "<|unused29|>",
    "<|unused30|>",
    "<|unused31|>",
    "<|unused32|>",
    "<|unused33|>",
    "<|unused34|>",
    "<|unused35|>",
    "<|unused36|>",
    "<|unused37|>",
    "<|unused38|>",
    "<|unused39|>",
    "<|unused40|>",
    "<|unused41|>",
    "<|unused42|>",
    "<|unused43|>",
    "<|unused44|>",
    "<|unused45|>",
    "<|unused46|>",
    "<|unused47|>",
    "<|unused48|>",
    "<|unused49|>",
    "<|unused50|>",
    "<0x00>",
    "<0x01>",
    "<0x02>",
    "<0x03>",
    "<0x04>",
    "<0x05>",
    "<0x06>",
    "<0x07>",
    "<0x08>",
    "<0x09>",
    "<0x0A>",
    "<0x0B>",
    "<0x0C>",
    "<0x0D>",
    "<0x0E>",
    "<0x0F>",
    "<0x10>",
    "<0x11>",
    "<0x12>",
    "<0x13>",
    "<0x14>",
    "<0x15>",
    "<0x16>",
    "<0x17>",
    "<0x18>",
    "<0x19>",
    "<0x1A>",
    "<0x1B>",
    "<0x1C>",
    "<0x1D>",
    "<0x1E>",
    "<0x1F>",
    "<0x20>",
    "<0x21>",
    "<0x22>",
    "<0x23>",
    "<0x24>",
    "<0x25>",
    "<0x26>",
    "<0x27>",
    "<0x28>",
    "<0x29>",
    "<0x2A>",
    "<0x2B>",
    "<0x2C>",
    "<0x2D>",
    "<0x2E>",
    "<0x2F>",
    "<0x30>",
    "<0x31>",
    "<0x32>",
    "<0x33>",
    "<0x34>",
    "<0x35>",
    "<0x36>",
    "<0x37>",
    "<0x38>",
    "<0x39>",
    "<0x3A>",
    "<0x3B>",
    "<0x3C>",
    "<0x3D>",
    "<0x3E>",
    "<0x3F>",
    "<0x40>",
    "<0x41>",
    "<0x42>",
    "<0x43>",
    "<0x44>",
    "<0x45>",
    "<0x46>",
    "<0x47>",
    "<0x48>",
    "<0x49>",
    "<0x4A>",
    "<0x4B>",
    "<0x4C>",
    "<0x4D>",
    "<0x4E>",
    "<0x4F>",
    "<0x50>",
    "<0x51>",
    "<0x52>",
    "<0x53>",
    "<0x54>",
    "<0x55>",
    "<0x56>",
    "<0x57>",
    "<0x58>",
    "<0x59>",
    "<0x5A>",
    "<0x5B>",
    "<0x5C>",
    "<0x5D>",
    "<0x5E>",
    "<0x5F>",
    "<0x60>",
    "<0x61>",
    "<0x62>",
    "<0x63>",
    "<0x64>",
    "<0x65>",
    "<0x66>",
    "<0x67>",
    "<0x68>",
    "<0x69>",
    "<0x6A>",
    "<0x6B>",
    "<0x6C>",
    "<0x6D>",
    "<0x6E>",
    "<0x6F>",
    "<0x70>",
    "<0x71>",
    "<0x72>",
    "<0x73>",
    "<0x74>",
    "<0x75>",
    "<0x76>",
    "<0x77>",
    "<0x78>",
    "<0x79>",
    "<0x7A>",
    "<0x7B>",
    "<0x7C>",
    "<0x7D>",
    "<0x7E>",
    "<0x7F>",
    "<0x80>",
    "<0x81>",
    "<0x82>",
    "<0x83>",
    "<0x84>",
    "<0x85>",
    "<0x86>",
    "<0x87>",
    "<0x88>",
    "<0x89>",
    "<0x8A>",
    "<0x8B>",
    "<0x8C>",
    "<0x8D>",
    "<0x8E>",
    "<0x8F>",
    "<0x90>",
    "<0x91>",
    "<0x92>",
    "<0x93>",
    "<0x94>",
    "<0x95>",
    "<0x96>",
    "<0x97>",
    "<0x98>",
    "<0x99>",
    "<0x9A>",
    "<0x9B>",
    "<0x9C>",
    "<0x9D>",
    "<0x9E>",
    "<0x9F>",
    "<0xA0>",
    "<0xA1>",
    "<0xA2>",
    "<0xA3>",
    "<0xA4>",
    "<0xA5>",
    "<0xA6>",
    "<0xA7>",
    "<0xA8>",
    "<0xA9>",
    "<0xAA>",
    "<0xAB>",
    "<0xAC>",
    "<0xAD>",
    "<0xAE>",
    "<0xAF>",
    "<0xB0>",
    "<0xB1>",
    "<0xB2>",
    "<0xB3>",
    "<0xB4>",
    "<0xB5>",
    "<0xB6>",
    "<0xB7>",
    "<0xB8>",
    "<0xB9>",
    "<0xBA>",
    "<0xBB>",
    "<0xBC>",
    "<0xBD>",
    "<0xBE>",
    "<0xBF>",
    "<0xC0>",
    "<0xC1>",
    "<0xC2>",
    "<0xC3>",
    "<0xC4>",
    "<0xC5>",
    "<0xC6>",
    "<0xC7>",
    "<0xC8>",
    "<0xC9>",
    "<0xCA>",
    "<0xCB>",
    "<0xCC>",
    "<0xCD>",
    "<0xCE>",
    "<0xCF>",
    "<0xD0>",
    "<0xD1>",
    "<0xD2>",
    "<0xD3>",
    "<0xD4>",
    "<0xD5>",
    "<0xD6>",
    "<0xD7>",
    "<0xD8>",
    "<0xD9>",
    "<0xDA>",
    "<0xDB>",
    "<0xDC>",
    "<0xDD>",
    "<0xDE>",
    "<0xDF>",
    "<0xE0>",
    "<0xE1>",
    "<0xE2>",
    "<0xE3>",
    "<0xE4>",
    "<0xE5>",
    "<0xE6>",
    "<0xE7>",
    "<0xE8>",
    "<0xE9>",
    "<0xEA>",
    "<0xEB>",
    "<0xEC>",
    "<0xED>",
    "<0xEE>",
    "<0xEF>",
    "<0xF0>",
    "<0xF1>",
    "<0xF2>",
    "<0xF3>",
    "<0xF4>",
    "<0xF5>",
    "<0xF6>",
    "<0xF7>",
    "<0xF8>",
    "<0xF9>",
    "<0xFA>",
    "<0xFB>",
    "<0xFC>",
    "<0xFD>",
    "<0xFE>",
    "<0xFF>",
];

pub const DEFAULT_STOKENS_REPLACES: [(&str, &str); 21] = [
    ("E", "<|end|>"),
    ("P", "<|padding|>"),
    ("I", "<|input|>"),
    ("G", "<|ego|>"),
    ("M", "<|me|>"),
    ("A", "<|mask|>"),
    ("Q", "<|question|>"),
    ("F", "<|find|>"),
    ("R", "<|search|>"),
    ("T", "<|think|>"),
    ("U", "<|run|>"),
    ("X", "<|execute|>"),
    ("K", "<|knowledge|>"),
    ("N", "<|sentiment|>"),
    ("Y", "<|summary|>"),
    ("O", "<|goal|>"),
    ("D", "<|todo|>"),
    ("V", "<|speak|>"),
    ("W", "<|write|>"),
    ("B", "<|remember|>"),
    ("Z", "<|save|>"),
];

pub const PUNCTUATIONS: [char; 629] = [
    '‘', '’', '“', '”', '（', '）', '［', '］', '【', '】', '゠', '＝', '「', '」', '『', '』',
    '〝', '〟', '〜', '｛', '｝', '<', '>', '-', '[', ']', '(', ')', '{', '}', '|', '+', '^', '_',
    /*' ', */ '\t', '\n', '!', '"', '#', '%', '&', '\'', '*', ',', '.', '/', ':', ';', '?',
    '@', '\\', '¡', '§', '¶', '·', '¿', ';', '·', '՚', '՛', '՜', '՝', '՞', '՟', '։', '׀', '׃', '׆',
    '׳', '״', '؉', '؊', '،', '؍', '؛', '؞', '؟', '٪', '٫', '٬', '٭', '۔', '܀', '܁', '܂', '܃', '܄',
    '܅', '܆', '܇', '܈', '܉', '܊', '܋', '܌', '܍', '߷', '߸', '߹', '࠰', '࠱', '࠲', '࠳', '࠴', '࠵', '࠶',
    '࠷', '࠸', '࠹', '࠺', '࠻', '࠼', '࠽', '࠾', '࡞', '।', '॥', '॰', '৽', '੶', '૰', '౷', '಄', '෴', '๏',
    '๚', '๛', '༄', '༅', '༆', '༇', '༈', '༉', '༊', '་', '༌', '།', '༎', '༏', '༐', '༑', '༒', '༔', '྅',
    '࿐', '࿑', '࿒', '࿓', '࿔', '࿙', '࿚', '၊', '။', '၌', '၍', '၎', '၏', '჻', '፠', '፡', '።', '፣', '፤',
    '፥', '፦', '፧', '፨', '᙮', '᛫', '᛬', '᛭', '᜵', '᜶', '។', '៕', '៖', '៘', '៙', '៚', '᠀', '᠁', '᠂',
    '᠃', '᠄', '᠅', '᠇', '᠈', '᠉', '᠊', '᥄', '᥅', '᨞', '᨟', '᪠', '᪡', '᪢', '᪣', '᪤', '᪥', '᪦', '᪨',
    '᪩', '᪪', '᪫', '᪬', '᪭', '᭚', '᭛', '᭜', '᭝', '᭞', '᭟', '᭠', '᯼', '᯽', '᯾', '᯿', '᰻', '᰼', '᰽',
    '᰾', '᰿', '᱾', '᱿', '᳀', '᳁', '᳂', '᳃', '᳄', '᳅', '᳆', '᳇', '᳓', '‖', '‗', '†', '‡', '•', '‣',
    '․', '‥', '…', '‧', '‰', '‱', '′', '″', '‴', '‵', '‶', '‷', '‸', '※', '‼', '‽', '‾', '⁁', '⁂',
    '⁃', '⁇', '⁈', '⁉', '⁊', '⁋', '⁌', '⁍', '⁎', '⁏', '⁐', '⁑', '⁓', '⁕', '⁖', '⁗', '⁘', '⁙', '⁚',
    '⁛', '⁜', '⁝', '⁞', '⳹', '⳺', '⳻', '⳼', '⳾', '⳿', '⵰', '⸀', '⸁', '⸆', '⸇', '⸈', '⸋', '⸎', '⸏',
    '⸐', '⸑', '⸒', '⸓', '⸔', '⸕', '⸖', '⸘', '⸙', '⸛', '⸞', '⸟', '⸪', '⸫', '⸬', '⸭', '⸮', '⸰', '⸱',
    '⸲', '⸳', '⸴', '⸵', '⸶', '⸷', '⸸', '⸹', '⸼', '⸽', '⸾', '⸿', '⹁', '⹃', '⹄', '⹅', '⹆', '⹇', '⹈',
    '⹉', '⹊', '⹋', '⹌', '⹍', '⹎', '⹏', '⹒', '、', '。', '〃', '〽', '・', '꓾', '꓿', '꘍', '꘎', '꘏',
    '꙳', '꙾', '꛲', '꛳', '꛴', '꛵', '꛶', '꛷', '꡴', '꡵', '꡶', '꡷', '꣎', '꣏', '꣸', '꣹', '꣺', '꣼', '꤮',
    '꤯', '꥟', '꧁', '꧂', '꧃', '꧄', '꧅', '꧆', '꧇', '꧈', '꧉', '꧊', '꧋', '꧌', '꧍', '꧞', '꧟', '꩜', '꩝',
    '꩞', '꩟', '꫞', '꫟', '꫰', '꫱', '꯫', '︐', '︑', '︒', '︓', '︔', '︕', '︖', '︙', '︰', '﹅',
    '﹆', '﹉', '﹊', '﹋', '﹌', '﹐', '﹑', '﹒', '﹔', '﹕', '﹖', '﹗', '﹟', '﹠', '﹡', '﹨',
    '﹪', '﹫', '！', '＂', '＃', '％', '＆', '＇', '＊', '，', '．', '／', '：', '；', '？', '＠',
    '＼', '｡', '､', '･', '𐄀', '𐄁', '𐄂', '𐎟', '𐏐', '𐕯', '𐡗', '𐤟', '𐤿', '𐩐', '𐩑', '𐩒', '𐩓', '𐩔', '𐩕',
    '𐩖', '𐩗', '𐩘', '𐩿', '𐫰', '𐫱', '𐫲', '𐫳', '𐫴', '𐫵', '𐫶', '𐬹', '𐬺', '𐬻', '𐬼', '𐬽', '𐬾', '𐬿', '𐮙',
    '𐮚', '𐮛', '𐮜', '𐽕', '𐽖', '𐽗', '𐽘', '𐽙', '𑁇', '𑁈', '𑁉', '𑁊', '𑁋', '𑁌', '𑁍', '𑂻', '𑂼', '𑂾', '𑂿',
    '𑃀', '𑃁', '𑅀', '𑅁', '𑅂', '𑅃', '𑅴', '𑅵', '𑇅', '𑇆', '𑇇', '𑇈', '𑇍', '𑇛', '𑇝', '𑇞', '𑇟', '𑈸', '𑈹',
    '𑈺', '𑈻', '𑈼', '𑈽', '𑊩', '𑑋', '𑑌', '𑑍', '𑑎', '𑑏', '𑑚', '𑑛', '𑑝', '𑓆', '𑗁', '𑗂', '𑗃', '𑗄', '𑗅',
    '𑗆', '𑗇', '𑗈', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐', '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁',
    '𑙂', '𑙃', '𑙠', '𑙡', '𑙢', '𑙣', '𑙤', '𑙥', '𑙦', '𑙧', '𑙨', '𑙩', '𑙪', '𑙫', '𑙬', '𑜼', '𑜽', '𑜾', '𑠻',
    '𑥄', '𑥅', '𑥆', '𑧢', '𑨿', '𑩀', '𑩁', '𑩂', '𑩃', '𑩄', '𑩅', '𑩆', '𑪚', '𑪛', '𑪜', '𑪞', '𑪟', '𑪠', '𑪡',
    '𑪢', '𑱁', '𑱂', '𑱃', '𑱄', '𑱅', '𑱰', '𑱱', '𑻷', '𑻸', '𑿿', '𒑰', '𒑱', '𒑲', '𒑳', '𒑴', '𖩮', '𖩯', '𖫵',
    '𖬷', '𖬸', '𖬹', '𖬺', '𖬻', '𖭄', '𖺗', '𖺘', '𖺙', '𖺚', '𖿢', '𛲟', '𝪇', '𝪈', '𝪉', '𝪊', '𝪋', '𞥞', '𞥟',
];

#[derive(Clone, Debug, PartialEq, Eq)]
#[macro_rules_attribute(impl_serde_type!)]
#[non_exhaustive]
pub struct TokenB {
    pub cap_token: String,
    pub caplock_token: String,
    pub space_replacement: char,
    pub japanese_space_replacement: char,
}

impl TokenB {}

impl PreTokenizer for TokenB {
    fn pre_tokenize(&self, pretokenized: &mut PreTokenizedString) -> Result<()> {
        pretokenized.split(|_size: usize, sn: NormalizedString| {
            let mut r = vec![];

            let ss = sn.get();
            let ac: AhoCorasick = AhoCorasick::new(DEFAULT_STOKENS_FINDS.iter()).unwrap();
            let mut lastpos = 0;
            for mat in ac.find_iter(ss) {
                let start = mat.start();
                let end = mat.end();
                // insert last one
                if start != lastpos {
                    r.push(NormalizedString::from(&ss[lastpos..start]));
                    println!("S{}E", &ss[lastpos..start]);
                }
                println!("{}", &ss[start..end]);
                r.push(NormalizedString::from(&ss[start..end]));
                lastpos = end;
            }
            if lastpos != ss.len() {
                r.push(NormalizedString::from(&ss[lastpos..]));
            }
            Ok(r)
        })?;

        pretokenized.split(|_size: usize, sn: NormalizedString| {
            let mut r = vec![];

            let mut last = 0;
            let mut cap = false;
            let mut caplock = false;

            let s = sn.get();

            if DEFAULT_STOKENS_FINDS.contains(&s) {
                if let Some(&v) = DEFAULT_STOKENS_MAP_REV.get(s) {
                    r.push(NormalizedString::from(v));
                }
                return Ok(r);
            } else if s == " " {
                r.push(NormalizedString::from("S"));
                return Ok(r);
            }

            let mut pos = 0;
            let mut ppos = 0;
            let mut cap_since = 0;
            for c in s.chars() {
                let clen = c.len_utf8();
                let cpos = pos + clen;
                if PUNCTUATIONS.contains(&c) {
                    if last < pos {
                        if caplock {
                            r.push(NormalizedString::from(self.caplock_token.as_str()));
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        } else if cap {
                            r.push(NormalizedString::from(self.cap_token.as_str()));
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        } else {
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        }
                    }
                    r.push(NormalizedString::from(&s[pos..cpos]));

                    last = cpos;
                    cap = false;
                    caplock = false;
                    cap_since = 0;
                }

                // whitespace
                if cap && c.is_whitespace() {
                    r.push(NormalizedString::from(self.cap_token.as_str()));
                    cap = false;
                    cap_since = 0;
                } else if caplock && c.is_whitespace() {
                    r.push(NormalizedString::from(self.caplock_token.as_str()));
                    caplock = false;
                    cap_since = 0;
                } else if !cap && !caplock && c.is_uppercase() {
                    // Start of the capital letter? -> Tokenize here if possible
                    if last < pos {
                        if caplock {
                            r.push(NormalizedString::from(self.caplock_token.as_str()));
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        } else if cap {
                            r.push(NormalizedString::from(self.cap_token.as_str()));
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        } else {
                            r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                        }
                    }
                    last = pos;
                    cap = true;
                    caplock = false;
                    cap_since = 1;
                } else if cap && cap_since == 1 && c.is_uppercase() {
                    // Another Letter with Captal Letter -> to CapLock
                    cap = false;
                    caplock = true;
                    cap_since += 1;
                } else if cap && c.is_uppercase() {
                    // Tokenize Here & restart?
                    if last < ppos {
                        r.push(NormalizedString::from(self.cap_token.as_str()));
                        r.push(NormalizedString::from(s[last..pos].to_lowercase()));
                    }
                    last = pos;
                    cap = true;
                    caplock = false;
                    cap_since = 1;
                } else if caplock && !c.is_uppercase() {
                    if last < ppos {
                        if cap_since == 2 {
                            r.push(NormalizedString::from(self.cap_token.as_str()));
                            r.push(NormalizedString::from(s[last..ppos].to_lowercase()));
                        } else {
                            r.push(NormalizedString::from(self.caplock_token.as_str()));
                            r.push(NormalizedString::from(s[last..ppos].to_lowercase()));
                        }
                    }
                    last = ppos;
                    caplock = false;
                    cap = true;
                    cap_since = 2;
                } else if caplock || cap {
                    cap_since += 1;
                }

                ppos = pos;
                pos = cpos;
            }
            // # Don't forget the last one
            if last < s.len() - 1 {
                if caplock {
                    r.push(NormalizedString::from(self.caplock_token.as_str()));
                    r.push(NormalizedString::from(s[last..].to_lowercase()));
                } else if cap {
                    r.push(NormalizedString::from(self.cap_token.as_str()));
                    r.push(NormalizedString::from(s[last..].to_lowercase()));
                } else {
                    r.push(NormalizedString::from(s[last..].to_lowercase()));
                }
            }

            Ok(r)
        })?;

        // Split the equal sign if longer than 4 because it's a tab size
        pretokenized.split(|_size: usize, os: NormalizedString| {
            let mut r = vec![];
            let s = os.get();
            if s.contains("====") {
                let mut start = 0;
                let mut ws_start = 0;
                let mut ws_cnt: i32 = -1;
                let mut pos = 0;
                for c in s.chars() {
                    let cpos = pos + c.len_utf8();
                    if c == '=' {
                        if ws_cnt == -1 {
                            ws_start = pos;
                            ws_cnt = 1;
                        } else {
                            ws_cnt += 1;
                        }
                    } else if ws_cnt > 3 {
                        if start != ws_start {
                            r.push(NormalizedString::from(&s[start..ws_start]));
                        }
                        while ws_cnt > 0 {
                            let cur_reduce = if ws_cnt < 4 { ws_cnt } else { 4 };
                            r.push(NormalizedString::from(
                                &s[ws_start..(ws_start + cur_reduce as usize)],
                            ));
                            ws_start += cur_reduce as usize;
                            ws_cnt -= cur_reduce;
                        }
                        // reset start to pos
                        start = pos;
                        ws_cnt = -1;
                    } else {
                        ws_cnt = -1;
                    }
                    pos = cpos;
                }

                if ws_cnt > 3 {
                    if start != ws_start {
                        r.push(NormalizedString::from(&s[start..ws_start]));
                    }
                    while ws_cnt > 0 {
                        let cur_reduce = if ws_cnt < 4 { ws_cnt } else { 4 };
                        r.push(NormalizedString::from(
                            &s[ws_start..(ws_start + cur_reduce as usize)],
                        ));
                        ws_start += cur_reduce as usize;
                        ws_cnt -= cur_reduce;
                    }
                    // reset start to pos
                } else {
                    r.push(NormalizedString::from(&s[start..]));
                }
            } else {
                r.push(os);
            }
            Ok(r)
        })?;

        // Split the space if longer than 4 because it's a tab size
        pretokenized.split(|_size: usize, os: NormalizedString| {
            let mut r = vec![];
            let s = os.get();
            if s.contains("     ") {
                let mut start = 0;
                let mut ws_start = 0;
                let mut ws_cnt: i32 = -1;
                let mut pos = 0;
                for c in s.chars() {
                    let cpos = pos + c.len_utf8();
                    if c == ' ' {
                        if ws_cnt == -1 {
                            ws_start = pos;
                            ws_cnt = 1;
                        } else {
                            ws_cnt += 1;
                        }
                    } else if ws_cnt > 3 {
                        if start != ws_start {
                            r.push(NormalizedString::from(&s[start..ws_start]));
                        }
                        while ws_cnt > 0 {
                            let cur_reduce = if ws_cnt < 4 { ws_cnt } else { 4 };
                            r.push(NormalizedString::from(
                                &s[ws_start..(ws_start + cur_reduce as usize)],
                            ));
                            ws_start += cur_reduce as usize;
                            ws_cnt -= cur_reduce;
                        }
                        // reset start to pos
                        start = pos;
                        ws_cnt = -1;
                    } else {
                        ws_cnt = -1;
                    }
                    pos = cpos;
                }

                if ws_cnt > 3 {
                    if start != ws_start {
                        r.push(NormalizedString::from(&s[start..ws_start]));
                    }
                    while ws_cnt > 0 {
                        let cur_reduce = if ws_cnt < 4 { ws_cnt } else { 4 };
                        r.push(NormalizedString::from(
                            &s[ws_start..(ws_start + cur_reduce as usize)],
                        ));
                        ws_start += cur_reduce as usize;
                        ws_cnt -= cur_reduce;
                    }
                    // reset start to pos
                } else {
                    r.push(NormalizedString::from(&s[start..]));
                }
            } else {
                r.push(os);
            }
            Ok(r)
        })?;

        // Replace spaces
        let replacement = self.space_replacement.to_string();
        let replacement_s = replacement.as_str();
        let japanese_replacement = self.japanese_space_replacement.to_string();
        let japanese_replacement_s = japanese_replacement.as_str();
        // Now replace whitespace
        pretokenized.normalize(|s| {
            s.replace(" ", replacement_s)?;
            s.replace("　", japanese_replacement_s)
        })
    }
}

impl PostProcessor for TokenB {
    fn added_tokens(&self, _is_pair: bool) -> usize {
        DEFAULT_STOKENS_STR.len()
    }

    // fn process(
    //     &self,
    //     encoding: tokenizers::Encoding,
    //     _pair_encoding: Option<tokenizers::Encoding>,
    //     _add_special_tokens: bool,
    // ) -> Result<tokenizers::Encoding> {
    //     println!("P - {:?}", encoding);
    //     Ok(encoding)
    // }

    fn process_encodings(
        &self,
        encodings: Vec<tokenizers::Encoding>,
        _add_special_tokens: bool,
    ) -> Result<Vec<tokenizers::Encoding>> {
        // let mut r = vec![];
        // for mut encoding in encodings {
        //     let mut modified = false;
        //     let mut speical_started = false;
        //     let mut possible_special = String::new();
        //     for (i, token) in encoding.get_tokens().iter().enumerate() {
        //         if !speical_started {
        //             if token.starts_with('<') {
        //                 possible_special += token;
        //             } else {
        //             }
        //         } else {
        //             let clen = possible_special.len();
        //             if clen == 1 {
        //                 if token.starts_with('|') {
        //                     possible_special += token;
        //                 } else {
        //                     speical_started = false;
        //                     possible_special = String::from("");
        //                 }
        //             }
        //         }
        //     }

        //     r.push(if modified { encoding } else { encoding });
        // }
        // encodings.iter().for_each(|(i, encoding)| {
        //     encoding.set_sequence_id(i);
        //     encoding
        //         .get_overflowing_mut()
        //         .iter_mut()
        //         .for_each(|encoding| encoding.set_sequence_id(i));
        //     encoding.set_type_ids(vec![i as u32; encoding.len()]);
        // });
        // println!("PE - {:?}", encodings);
        // Ok(encodings)
        Ok(encodings)
    }
}

impl Decoder for TokenB {
    fn decode(&self, tokens: Vec<String>) -> Result<String> {
        let mut r = String::new();
        let mut cap = false;
        let mut caplock = false;
        let mut bytebuf = vec![];
        let replacement = self.space_replacement.to_string();
        let replacement_str = replacement.as_str();
        let japanese_replacement = self.japanese_space_replacement.to_string();
        let japanese_replacement_s = japanese_replacement.as_str();
        for token in tokens.iter() {
            // TODO:: after Caplock or Capital -> Upper until a whitespace or a punchuation
            let token_str = token.as_str();
            if token_str.len() == 1 {
                if let Some(&o) = DEFAULT_STOKENS_MAP.get(token_str) {
                    r += o;
                    caplock = false;
                    cap = false;
                    continue;
                }
            }
            if token_str.len() == 6 && token_str.starts_with("<0x") && token_str.ends_with('>') {
                let to_parse = &token_str[3..5];
                if let Ok(n) = u8::from_str_radix(to_parse, 16) {
                    bytebuf.push(n);
                    continue;
                }
            } else if !bytebuf.is_empty() {
                if let Ok(v) = std::str::from_utf8(bytebuf.as_slice()) {
                    r += v;
                }
            }

            if cap {
                let mut s = String::new();
                let ctoken = token.as_str();
                let mut ftokenpos = 0;
                for (i, c) in token.chars().enumerate() {
                    if i == 0 {
                        ftokenpos = c.len_utf8();
                        s += ctoken[0..ftokenpos]
                            .replace(replacement_str, " ")
                            .replace(japanese_replacement_s, "　")
                            .to_uppercase()
                            .as_str();
                    } else {
                        s += &ctoken[ftokenpos..]
                            .replace(replacement_str, " ")
                            .replace(japanese_replacement_s, "　");
                        break;
                    }
                }
                r += s.as_str();
                cap = false;
            } else if caplock {
                let mut endpos = 0;
                if token == "C" || token == "L" {
                    continue;
                }
                for c in token.chars() {
                    if c == 'S' || PUNCTUATIONS.contains(&c) {
                        caplock = false;
                        break;
                    } else {
                        endpos += c.len_utf8();
                    }
                }
                let ctoken = token.as_str();
                if endpos != tokens.len() {
                    r += ctoken[..endpos]
                        .replace(replacement_str, " ")
                        .replace(japanese_replacement_s, "　")
                        .to_uppercase()
                        .as_str();
                    r += &ctoken[endpos..]
                        .replace(replacement_str, " ")
                        .replace(japanese_replacement_s, "　");
                } else {
                    r += ctoken[0..]
                        .replace(replacement_str, " ")
                        .replace(japanese_replacement_s, "　")
                        .to_uppercase()
                        .as_str();
                }
            } else if self.caplock_token.eq(token) {
                caplock = true;
            } else if self.cap_token.eq(token) {
                cap = true;
            } else {
                r += token
                    .replace(replacement_str, " ")
                    .replace(japanese_replacement_s, "　")
                    .as_str();
            }
        }

        if !bytebuf.is_empty() {
            if let Ok(v) = std::str::from_utf8(bytebuf.as_slice()) {
                r += v;
            }
        }
        Ok(r)
    }

    fn decode_chain(&self, tokens: Vec<String>) -> Result<Vec<String>> {
        Ok(tokens)
    }
}

impl Default for TokenB {
    fn default() -> Self {
        Self {
            cap_token: String::from("C"),
            caplock_token: String::from("L"),
            space_replacement: 'S',
            japanese_space_replacement: 'J',
        }
    }
}
