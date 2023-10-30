use pyo3::{prelude::*, wrap_pyfunction};
use pyo3::exceptions::{PyIOError, PyFileNotFoundError};

use std::path::Path;
use futures::StreamExt;

use chromiumoxide::browser::{Browser, BrowserConfig};
use chromiumoxide::cdp::browser_protocol::page::PrintToPdfParams;

const PATH_PREFIX: &str = "File://";

#[pyfunction]
fn convert<'p>(
    py: Python<'p>, 
    input_path: &'p PyAny,
    output_path: &'p PyAny,
    chromeium_path: Option<&'p PyAny>  ) -> PyResult<&'p PyAny> {
    
    // Get the input parameters - think I can use unwrap here since extract should work?
    let input_path: String = input_path.extract().unwrap();
    let output_path: String = output_path.extract().unwrap();

    // Check the input path exists
    if !Path::new(&input_path).exists(){
        return Err(PyFileNotFoundError::new_err("Input path does not exist: {input_path}"))
    }

    // Create the BrowserConfig
    let config_result: Result<BrowserConfig, String> = match chromeium_path{
        Some(v) => {
            let path: String = v.extract()?;
            match Path::new(&path).exists() as bool{
                true => BrowserConfig::builder().chrome_executable(path).build(),
                false => Err("Chromeium Executable path does not exist".to_owned())
            }
        },
        _ => BrowserConfig::builder().build()
    };

    // Find the config result
    let config = match config_result {
        Ok(v) => v,
        Err(e) => return Err(PyFileNotFoundError::new_err(e))
    };

    // Conversion to pdf from html which is async
    pyo3_asyncio::tokio::future_into_py_with_locals(
        py,
        pyo3_asyncio::tokio::get_current_locals(py)?,
        async move {
            
            // Create the browser instance
            let (browser, mut handler) = Browser::launch(config).await.unwrap();
            
            // Create the thread handle
            let _handle = tokio::task::spawn(async move {
                while let Some(h) = handler.next().await {
                    if h.is_err() {
                        break;
                    }
                }
            });

            // Open the input file
            let page_res = browser
                .new_page(PATH_PREFIX.to_owned() + &input_path)
                .await;
            
            // Error handling for not able to open input file
            let page = match page_res {
                Ok(v) => v,
                Err(e) => return Err(PyIOError::new_err(e.to_string())) 
            };
            
            // Save the html to pdf
            if let Err(e) = page.save_pdf(PrintToPdfParams::default(), &output_path).await {
                return Err(PyIOError::new_err(e.to_string()))
            }

            // Close the page
            page.close().await.unwrap();

            // Exit with a succesful
            Python::with_gil(|py| Ok(py.None()))
        }
    )
}
    


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn html2pdf(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert, m)?)?;
    Ok(())
}