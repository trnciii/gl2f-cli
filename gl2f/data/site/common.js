function tileMedia(mediaList, width, columns, showList)
{
  const itemWidth = width/columns;

  const element = document.createElement('center');

  if(showList)
  {
    const min = 250;

    const list = document.createElement('div');
    list.className = 'tile';
    list.style.marginTop = '20px';
    list.style.marginBottom = '20px';
    list.innerHTML = `<div style="padding:20px; background: pink;text-align:left;">${mediaList.map(i=>`<div class=list-item>${i}</div>`).join('')}</div>`

    element.appendChild(list);
    element.appendChild(document.createElement('br'));
  }

  mediaList.map(i => `contents/${i}`)
    .map(src => {
      const ext = src.slice(src.lastIndexOf('.'));
      if([".jpeg", ".png"].indexOf(ext) > -1){
        return `<a class="image" data-group="gallery" href=${src}><img src="${src}" width=${itemWidth}/></a>`;
      }
      else if([".mp4"].indexOf(ext) > -1){
        return `<a class="iframe" href=${src}><video controls autoplay muted loop src="${src}" width=${itemWidth}/></a>`;
      }
      else if([".mov"].indexOf(ext) > -1){
        return `<video controls autoplay muted loop src="${src}" width=${itemWidth} />`;
      }
      else{
        alert(`Unknown media file: ${src}`);
        return '';
      }
    })
    .forEach(t => {
      const i = document.createElement('div');
      i.className = 'tile';
      i.innerHTML = t;
      element.appendChild(i);
    });

  return element;
}

function setupModaal()
{
  $('.image').modaal({
    type: 'image',
    hide_close: true,
  })
  $('.iframe').modaal({
    type: 'iframe',
    hide_close: true,
  });
}