import React from 'react';
import 'tachyons';
class App extends React.Component {
 constructor(props) {
    super();
    //this.handlePlay = this.handlePlay.bind(this);
    this.state=
    {
      file:null,
      preds:"",
    }
  }
  handleFileChange = (event) => {
      if (event.target.files[0]) {
          this.setState({ file: event.target.files[0] });
      }
  }
  // handlePlay() {
  //   if(this.state.file!=null)
  //   {
  //     let audio = new Audio(sound);
  //     var playPromise = audio.play();

  //           if (playPromise !== undefined) {
  //             playPromise
  //               .then(_ => {
  //                 // Automatic playback started!
  //                 // Show playing UI.
  //                 console.log("audio played auto");
  //               })
  //               .catch(error => {
  //                 // Auto-play was prevented
  //                 // Show paused UI.
  //                 console.log("playback prevented");
  //               });
  //           }
  //     }
  // }
  handleSubmit=()=>
    {
    var formData = new FormData();
    let files=this.state.file;
    formData.append(1, files);
    
    fetch('http://127.0.0.1:5000/upload', {
      // content-type header should not be specified!
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(success => {
        // console.log(success)
        this.setState({preds:success.preds})
        // Do something with the successful response
      })
      .catch(error => console.log(error)
    );
    this.setState({file:null,})
  }
  render() {
    return (
            <div className="cover ss "><article className="br3 ba b--black-10 mv4 tc w-00  w-40-l mw6 shadow-5 center main">
                <main className="pa4 black-80">
                    <div className="measure">
                        <fieldset id="sign_up" className="ba b--transparent ph0 mh0">
                            <legend className="f1 fw6 ph0 mh0">Upload File</legend>
                            <div className="mt3 center">
                                <label className="db fw6 lh-copy f4" htmlFor="name">Choose File</label>
                                <input
                                    className="pa1 input-reset ba bg-transparent hover-bg-black hover-white "
                                    type="file"
                                    name="file"
                                    id="name"
                                    onChange={this.handleFileChange}
                                />
                            </div>
                        </fieldset>
                        <div >
                            <input
                                onClick={this.handleSubmit}
                                className="b ph3 pv2 br3 input-reset ba b--black bg-transparent grow pointer f6 dib"
                                type="submit"
                                value="Predict"
                            />
                        </div>
                    </div>
                    {
                      this.state.preds.length?<h2>Predicted : {this.state.preds}</h2>:<h2/>
                    }
                </main>

            </article></div>
    );
  }
}

export default App;