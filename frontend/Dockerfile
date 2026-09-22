FROM denoland/deno:2.7.12 AS base

WORKDIR /app

COPY package.json .
COPY deno.lock .
COPY deno.json .

RUN deno install --allow-scripts

COPY . .

### DEV [CURRENTLY NOT USED] ###
# FROM base AS dev
# # COPY . .
# EXPOSE 3000
# RUN deno task build
# # CMD ["run", "-A", "npm:vite", "dev", "--host"]
# CMD ["deno", "task", "dev", "--host", "0.0.0.0"]
###

### PROD ###
FROM base AS build
RUN deno task build


FROM denoland/deno:2.7.12 AS production

WORKDIR /app

# COPY --from=build . .
COPY --from=build /app/package.json .
COPY --from=build /app/deno.lock .
COPY --from=build /app/build ./build
COPY --from=build /app/node_modules ./node_modules

EXPOSE 3000

CMD ["run", "--allow-net", "--allow-read", "--allow-env", "./build/index.js"]
