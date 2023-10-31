mod tokenb;

use tokenizers::{
    models::bpe::{BpeBuilder, BPE},
    normalizers::{NormalizerWrapper, NFC, NFD},
    tokenizer::TokenizerImpl,
    Result, TokenizerBuilder,
};

pub use tokenb::TokenB;
pub use tokenb::DEFAULT_STOKENS;
pub use tokenb::PUNCTUATIONS;

pub type TokenBTokenizer = TokenizerImpl<BPE, NormalizerWrapper, TokenB, TokenB, TokenB>;

pub fn new(normalizer: &str) -> Result<TokenBTokenizer> {
    let normalizer = if normalizer == "nfd" {
        NormalizerWrapper::NFD(NFD)
    } else {
        NormalizerWrapper::NFC(NFC)
    };
    TokenizerBuilder::new()
        .with_model(
            BpeBuilder::default()
                .unk_token(String::from("<|unknown|>"))
                .byte_fallback(true)
                .build()?,
        )
        .with_normalizer(Some(normalizer))
        .with_pre_tokenizer(Some(TokenB::default()))
        .with_post_processor(Some(TokenB::default()))
        .with_decoder(Some(TokenB::default()))
        .build()
}

pub fn load_from_file(path: String) -> Result<TokenBTokenizer> {
    let data = std::fs::read_to_string(path).map_err(|e| tokenizers::Error::from(e.to_string()))?;
    let json: serde_json::Value = serde_json::from_str(data.as_str()).unwrap();

    let mut vocab = std::collections::HashMap::new();
    let mut merges = vec![];

    if let (Some(v), Some(m)) = (
        json.get("model")
            .and_then(|f| f.get("vocab"))
            .and_then(|f| f.as_object())
            .map(|f| {
                f.iter()
                    .map(|(k, v)| (k.clone(), v.as_u64().unwrap() as u32))
                    .collect::<std::collections::HashMap<String, u32>>()
            }),
        json.get("model")
            .and_then(|f| f.get("merges"))
            .and_then(|f| f.as_array())
            .map(|f| {
                f.iter()
                    .map(|a| a.as_str().unwrap_or_default().to_string())
                    .collect::<Vec<String>>()
            }),
    ) {
        vocab = v;
        for v in m.iter() {
            let aa = v.split(' ').collect::<Vec<&str>>();
            if aa.len() != 2 {
                return Err(tokenizers::Error::from("merges are faulty"));
            } else {
                if !vocab.contains_key(aa[0]) {
                    return Err(tokenizers::Error::from(format!(
                        "merged token oov {} o: {} {}",
                        aa[0], aa[0], aa[1]
                    )));
                }
                if !vocab.contains_key(aa[1]) {
                    return Err(tokenizers::Error::from(format!(
                        "merged token oov {} o: {} {}",
                        aa[1], aa[0], aa[1]
                    )));
                }

                let new_token = format!("{}{}", aa[0], &aa[1][0..]);
                if !vocab.contains_key(&new_token) {
                    return Err(tokenizers::Error::from(format!(
                        "merged token new_token oov {} o: {} {}",
                        new_token, aa[0], aa[1]
                    )));
                }

                merges.push((aa[0].to_string(), aa[1].to_string()));
            }
        }
    }

    let normalizer = if json
        .get("normalizer")
        .and_then(|f| f.get("type"))
        .and_then(|f| f.as_str())
        .map(|f| f.to_string())
        .unwrap_or(String::from("nfc"))
        == "nfd"
    {
        NormalizerWrapper::NFD(NFD)
    } else {
        NormalizerWrapper::NFC(NFC)
    };

    let tokenizer = TokenizerBuilder::new()
        .with_model(
            BpeBuilder::default()
                .vocab_and_merges(vocab, merges)
                .unk_token(String::from("<|unknown|>"))
                .byte_fallback(true)
                .build()
                .unwrap(),
        )
        .with_normalizer(Some(normalizer))
        .with_pre_tokenizer(Some(TokenB::default()))
        .with_post_processor(Some(TokenB::default()))
        .with_decoder(Some(TokenB::default()))
        .build()?;

    Ok(tokenizer)
}

#[cfg(test)]
#[test]
fn encode_test() {
    let tokenizer = load_from_file(String::from("../../results/tokenizer_32000_nfc.json")).unwrap();
    // let tokenizer = load_from_file(String::from(
    //     "../../results/original/tokenizer_37720_nfc.json",
    // ))
    // .unwrap();
    let encoding = tokenizer
        .encode(
            "CAPITAL<|me|><|input|><|mask|>Select this! SElect SELect. 한글은 어떻게 처리하니? ㅋㅋㅋ",
            true,
        )
        .unwrap();
    println!("{:?}", encoding.get_ids());
    println!("{:?}", encoding.get_tokens());
    let ids = encoding.get_ids();
    let decoding = tokenizer.decode(ids, false).unwrap();
    println!("{}", decoding);
}
