const SHOPEE_AFFILIATE_ID = process.env.NEXT_PUBLIC_SHOPEE_AFFILIATE_ID || "";
const SHOPEE_REDIR_BASE = "https://s.shopee.co.id/an_redir";

export function toAffiliateLink(url: string, subId?: string): string {
  if (!SHOPEE_AFFILIATE_ID) return url;
  if (!url || !url.includes("shopee.co.id")) return url;
  if (url.includes("affiliate_id=")) return url;

  const params = new URLSearchParams({
    origin_link: url,
    affiliate_id: SHOPEE_AFFILIATE_ID,
  });

  if (subId) {
    params.set("sub_id", subId);
  }

  return `${SHOPEE_REDIR_BASE}?${params.toString()}`;
}
