'use strict';

const PaperLite = props => {
    const p = props.paper;
    return (
    <div class='rel_paper'>
        <div class='rel_title'><a href={p.link}>{p.title}</a></div>
        <div class='rel_authors'>{p.authors}</div>
        <div class='rel_time'>{p.time}</div>
        <div class='rel_tags'>{p.tags}</div>
        <div class='rel_abs'>{p.summary}</div>
        <div class='rel_code'><a href={p.link}>Code</a></div>
    </div>
    )
}

ReactDOM.render(<PaperLite paper={paper} />, document.getElementById('wrap'))
