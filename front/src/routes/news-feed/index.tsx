import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";

export interface News {
  id: number;
  logo: string;
  location: string;
  title: string;
  category: string;
  startup_id: string;
  description: string;
  news_date: Date;
}

function Newss({ news }: { news: News }) {
  return (
    <div className="News" key={news.id}>
      <h3>{news.title}</h3>
      <p>{news.description}</p>
      <div className="news-meta">
        <span>Date: {news.news_date.toString()}</span>
        <br />
        <span>Location: {news.location}</span>
        <br />
      </div>
      <img
        src={`${API_BASE_URL}/api/news/${news.id}/image`}
        alt={news.title}
        width="600px"
        height="400px"
        className="news-logo"
        onError={(e) => {
          (e.currentTarget as HTMLImageElement).src =
            "https://placehold.co/600x400/EED5FB/31343C";
        }}
      />
    </div>
  );
}

export default function NewsPage() {
  const [news, setNews] = useState<News[] | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/news/`)
      .then((res) => res.json())
      .then((list: News[]) => setNews(list))
      .catch(console.error);
  }, []);

  if (news === null) {
    return (
      <section className="news-feed">
        <h2>News</h2>
        <div className="news-list">
          <p>Loading news...</p>
        </div>
      </section>
    );
  }

  if (news.length === 0) {
    return (
      <section className="news-feed">
        <h2>News</h2>
        <div className="news-list">
          <p>No news available at the moment.</p>
        </div>
      </section>
    );
  }

  const grouped = news.reduce<Record<string, News[]>>((acc, item) => {
    const category = item.category || "Uncategorized";
    if (!acc[category]) acc[category] = [];
    acc[category].push(item);
    return acc;
  }, {});

  return (
    <section className="news-feed space-y-8">
      <h2>News</h2>

      {Object.entries(grouped).map(([category, items]) => {
        const sortedItems = [...items].sort(
          (a, b) =>
            new Date(b.news_date).getTime() - new Date(a.news_date).getTime()
        );

        return (
          <div key={category}>
            <h3 className="text-xl font-semibold">{category}</h3>
            <div className="news-list grid grid-cols-3 gap-4">
              {sortedItems.map((n) => (
                <Newss key={n.id} news={n} />
              ))}
            </div>
          </div>
        );
      })}
    </section>
  );
}
