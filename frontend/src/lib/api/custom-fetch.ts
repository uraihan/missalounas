const getUrl = (contextUrl: string): string => {
  const url = new URL(contextUrl);
  const pathname = url.pathname;
  const search = url.search;
  const baseUrl = process.env.DEPLOY_ENV === "PROD"
    ? "http://backend:8010"
    : "http://localhost:3000";

  const requestUrl = new URL(`${pathname}${search}`, baseUrl);

  return requestUrl.toString();
};

export const customFetch = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  // const requestUrl = getUrl(url);
  const baseUrl = getUrl(url);
  const response = await fetch(baseUrl, options);

  const body = [204, 205, 304].includes(response.status)
    ? null
    : await response.text();
  const data = body ? JSON.parse(body) : {};

  return { data, status: response.status, headers: response.headers } as T;
};
