use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
pub struct TokenBTokenizer {
    pub(crate) inner: libtokenb::TokenBTokenizer,
}

#[pymethods]
impl TokenBTokenizer {
    #[new]
    fn new(normalizer: String) -> Self {
        TokenBTokenizer {
            inner: libtokenb::new(normalizer.as_str()).unwrap(),
        }
    }

    pub fn encode(&self, input: String) -> PyResult<Vec<u32>> {
        let encoded = self
            .inner
            .encode(input, true)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        let ids = encoded.get_ids().to_vec();
        Ok(ids)
    }

    pub fn decode(&self, input: Vec<u32>) -> PyResult<String> {
        let decoded = self
            .inner
            .decode(&input[..], false)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(decoded)
    }
}

#[pyfunction]
pub fn load_from_file(filename: String) -> PyResult<TokenBTokenizer> {
    let tokenizer =
        libtokenb::load_from_file(filename).map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(TokenBTokenizer { inner: tokenizer })
}
