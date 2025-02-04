/*
    Verwendet der Gallerie:
    Möglichkeit 1. - HTML-Elemente mit Klasse galImg in Container mit id gallery:

    - Der Container füür die Gallerie muss die id 'gallery' haben.
    - In dem Container werden <img> Elemente mit der Klasse galImg und dem src-Attribut angegeben.
    - Am Ende des <body> Elements wird das Skript gal.js mit dem Attribut type="module" eingebunden.
    - Außerdem muss die CSS-Datei gal.css eingebunden werden.
    - Animationsgeschwindigkeit kann mit der Variable animationDuration im Skript verändert werden.

    Möglichkeit 2. - Gallery-Objekt erzeugen:

    - Es muss das Skript gal.js am Ende des <body>-Elements mit dem Attribut type="module" eingebunden werden.
    - Es muss ein weiteres <script>-Tag gesetzt werden in dem Gallery von './gal.js' importiert wird und ein neues Gallery-Objekt erzeugt wird.
    - Syntax für das Gallery-Objekt: const gallerie = new Gallery('[ID des zu verwendenden Containers], ['bild1.jpg'], ['bild2.jpg'], ['bild3.jpg'], ...')
    - Es muss die CSS-datei gal.css eingebunden werden.
*/






class Gallery extends HTMLElement {

    constructor(galleryContainer, ...args) {
        super();


        this.attachShadow({ mode: 'open' });
        this.imgs = [];
        document.addEventListener('DOMContentLoaded', () => {
            this.autoScroll = true;
            this.autoScrollInterval = 4000;


            let style = document.createElement('style');
            style.textContent = `
            :root{
                --galWidthAnim: 0px;
            }
            
            *{
                box-sizing: border-box;
                margin: 0;
            }
            
            .test{
                width: 500px;
                height: 500px;
                background-color: blue;
            }
            
            main{
                width: 50vw;
                height: 100vh;
                margin: auto;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            #gallery{
                position: relative;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: rgba(128, 128, 128, 0.379);
            }
            
            .hide{
                display: none;
            }
            
            #prev, #next{
                position: absolute;
                height: 100%;
                width: 40%;
                cursor: pointer;
                z-index: 100;
            }
            
            #prev{
                left: 0;
            }
            
            #next{
                right: 0;
            }
            
            #prev:hover{
                background-image: linear-gradient(to right, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0));   
            }
            
            #next:hover{
                background-image: linear-gradient(to left, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0));   
             
            }
            
            @keyframes slideIn{
                0%{left: 100%;
                     
                }
                100%{left: 0px;
                   
                }
            }
            
            @keyframes slideOut{
                0%{
                    transform: (0px, 0px);
                    position: absolute;
                }
                100%{
                    transform: translate(var(--galWidthAnim), 0px);
                    position: absolute;
                }
            }
            
            
            
            .slideIn{
                animation-name: slideIn;
                animation-duration: 1s;
                animation-fill-mode: forwards;
            }
            
            .slideOut{
                animation-name: slideOut;
                animation-duration: 1s;
                animation-fill-mode: forwards;
            }
            @keyframes slideInL{
                0%{left: -100%;
                     
                }
                100%{left: 0px;
                   
                }
            }
            
            @keyframes slideOutL{
            
                0%{
                    transform: translate(0px, 0px);
                    position: absolute;
                }
                100%{
                    transform: translate(var(--galWidthAnim), 0px);
                    position: absolute;
                }
            }
            
            
            
            .slideInL{
                animation-name: slideInL;
                animation-duration: 1s;
                animation-fill-mode: forwards;
            }
            
            .slideOutL{
                animation-name: slideOutL;
                animation-duration: 1s;
                animation-fill-mode: forwards;
            }
            
            
            
            .galImg{
                position: relative;
            }
            `;

            this.galContainer = document.createElement('div');
            this.galContainer.id = 'gallery';

            this.shadowRoot.appendChild(style);
            this.shadowRoot.appendChild(this.galContainer);


            this.galNext = document.createElement('div');
            this.galNext.id = 'next';

            this.galPrev = document.createElement('div');
            this.galPrev.id = 'prev';
        });

    }

    connectedCallback() {
        document.addEventListener('DOMContentLoaded', () => {

            const prom = () => {
                const promise = new Promise((res, rej) => {



                    if (this.hasAttribute('imgs')) {
                        let bilder = this.getAttribute('imgs').replace(/ /g, '').split(',');
                        console.log(bilder);

                        for (let element of bilder) {
                            let bild = document.createElement('img');
                            bild.setAttribute('src', element);
                            bild.className = 'galImg';
                            bild.setAttribute('height', '100%');
                            bild.setAttribute('width', 'auto');
                            this.imgs.push(bild);

                            this.galContainer.appendChild(bild);

                        }

                        /* console.log('imgs', this.imgs); */
                    }



                    this.imgLength = this.imgs.length;
                    this.imgCount = this.imgs.length;
                    this.imgNum = this.imgCount % this.imgLength;
                    this.img = this.imgs[this.imgNum];

                    console.log("testA");
                    
                    // Mur der else-block muss da sein. this.gallery kann durch neu erstellten container ersetzt werden.

                    this.gallery = this.galContainer;
                    this.gallery.appendChild(this.galNext);
                    this.gallery.appendChild(this.galPrev);


                    this.inAnimation = false;


                    setInterval(() => {
                        if (this.autoScroll) {
                            if (!this.inAnimation) {
                                this.next();
                            }
                        }
                    }, this.autoScrollInterval)



                    //Hier muss next und prev erzeugt werden.
                    const next = this.galNext;
                    const prev = this.galPrev;



                   

                    

                    window.addEventListener('resize', () => {
                        this.checkSize(this.img);
                    });
                    this.animationDuration = 1;

                    this.imgs.forEach(element => {
                        element.style.animationDuration = `${this.animationDuration}s`;
                    });

                    for (let i = 0; i < this.imgLength; i++) {
                        if (i != this.imgNum) {
                            this.imgs[i].classList.add("hide");
                        }
                    }





                    this.next = () => {
                        if (!this.inAnimation) {
                            this.img.classList.remove("slideIn");
                            this.img.classList.remove("slideInL");
                            this.img.style.setProperty('--galWidthAnim', `-${this.gallery.offsetWidth}px`);


                            this.img.classList.add("slideOut");
                            ++this.imgCount
                            this.changeImg("right");

                        }
                    }

                    setTimeout(()=>{
                    this.checkSize(this.img);
                    }, 1000
                );

                    next.addEventListener("click", () => {
                        this.autoScroll = false;
                        this.next();
                    });


                    prev.addEventListener("click", () => {
                        this.autoScroll = false;
                        this.prev();
                    });

                    this.prev = () => {

                        if (!this.inAnimation) {
                            this.img.classList.remove("slideInL");
                            this.img.classList.remove("slideIn");
                            this.img.style.setProperty('--galWidthAnim', `${this.gallery.offsetWidth}px`);
                            console.log(this.gallery.offsetWidth);
                            this.img.classList.add("slideOutL");
                            this.imgCount = this.imgCount == 0 ? (this.imgLength - 1) : --this.imgCount;

                            this.changeImg("left");
                        }

                    }
                    res();
                });
                return promise;
            }
            prom().then(() => {
                console.log('then', this.img);
                this.checkSize(this.img);
                this.changeImg();
            });
            /* this.checkSize(this.img); */
            
        });

        






    }



    checkSize(img) {
        /* console.log('imgs', this.imgs);
        console.log('imgLength', this.imgLength);
        console.log('imgCount', this.imgCount);
        console.log('img', this.img);
        console.log('imgH', this.img.width);
        console.log('imgW', this.img.height); */

        console.log('testB', img);
        if (img.height > img.width) {
            img.setAttribute("width", "auto");
            img.setAttribute("height", "100%");

            let newWidth = img.offsetWidth;
            if (newWidth > this.gallery.offsetWidth) {
                img.setAttribute("width", "100%");
                img.setAttribute("height", "auto");
            }
        }

        if (img.height < img.width) {
            img.setAttribute("width", "100%");
            img.setAttribute("height", "auto");

            let newHeight = img.offsetHeight;
            if (newHeight > this.gallery.offsetHeight) {
                img.setAttribute("width", "auto");
                img.setAttribute("height", "100%");
            }
        }

    }

    timeoutP(time, callBack) {
        return new Promise((res, rej) => {
            try {
                setTimeout(() => {
                    callBack();
                    res("Timeout nach " + time + "ms abgeschlossen.")
                }, time);
            } catch (e) {
                rej("Error! ", e);
            }
        });
    }

    

    changeImg(direction) {

        this.imgNum = this.imgCount % this.imgLength;
        this.img = this.imgs[this.imgNum];
        this.inAnimation = true;

        //console.log('changeImg', "imgLen: ", this.imgLength, "imgCount: ", this.imgCount, "imgNum: ", this.imgNum, "img: ", this.img);

        this.timeoutP((this.animationDuration * 1000), () => {
            for (let i = 0; i < this.imgLength; i++) {
                if (i != this.imgNum) {
                    this.imgs[i].classList.add("hide");
                }
            }
            this.inAnimation = false;
        });

        this.img.classList.remove("hide");
        this.animateSlideIn(direction);


        this.checkSize(this.img);

    }

    animateSlideIn(direction) {
        if (direction == "right") {
            this.img.classList.remove("slideOut");
            this.img.classList.remove("slideOutL");
            this.img.classList.add("slideIn");
        }

        if (direction == "left") {
            this.img.classList.remove("slideOutL");
            this.img.classList.remove("slideOut");
            this.img.classList.add("slideInL");
        }
    }


}


/* if(document.getElementsByClassName('galImg').length > 0){
    console.log(document.getElementsByClassName('galImg'), "hi");
    const gallery = new Gallery();
} */

customElements.define('my-gallery', Gallery);

























