FROM denoland/deno:2.7.12 AS build

WORKDIR /app

COPY package.json .
COPY deno.lock .

RUN deno install --allow-scripts

COPY . .

RUN deno task build


FROM denoland/deno:2.7.12

WORKDIR /app

COPY --from=build . .
# COPY --from=build /app/package.json .
# COPY --from=build /app/deno.lock .
# COPY --from=build /app/build ./build
# COPY --from=build /app/node_modules ./node_modules

EXPOSE 3000

CMD ["run", "--allow-net", "--allow-read", "--allow-env", "./build/index.js"]
