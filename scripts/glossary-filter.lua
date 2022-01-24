function Str(el)
    paren, plus, link, back = el.text:match(
        "^(%(*)(%+)(%w+[_%-]*%w*[_%-]*%w*)(%g*)"
    )

    if link ~= "" and link ~= nil then 
        return pandoc.Link(string.format("%s%s%s", paren, link, back), string.format("#%s", string.lower(link)))
    else 
        return el
    end
end

