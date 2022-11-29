import React from "react";
import {
  Typography,
  Grid,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  CircularProgress,
} from "@mui/material";
import { ChevronDown } from "mdi-material-ui";
import ErrorBox from "components/misc/ErrorBox";

function ResultSummary({
  entityName,
  entityNamePlural,
  count,
  loading,
  errors = {},
  addOn,
}) {
  return (
    <AccordionSummary
      expandIcon={<ChevronDown sx={!count ? { display: "none" } : {}} />}
    >
      <Typography
        sx={{
          typography: { xs: "h5", sm: "h4" },
          opacity: count === 0 ? 0.38 : undefined,
        }}
      >
        {`${loading ? "?" : count || 0} ${
          count && count > 1 ? entityNamePlural : entityName
        }`}
        {loading && (
          <CircularProgress color="secondary" size="24px" sx={{ ml: 2 }} />
        )}
      </Typography>
      <ErrorBox errorDict={errors} />
      {addOn}
    </AccordionSummary>
  );
}

function AdditionalResults({ remaining_result_count, entityNamePlural }) {
  return (
    <Typography
      variant="body1"
      color="textSecondary"
      align="right"
      sx={{ mx: 2, mb: 1 }}
    >{`... et ${remaining_result_count} autres ${entityNamePlural}.`}</Typography>
  );
}

function ResultsList({ results, CardComponent }) {
  return (
    <Grid container sx={{ mb: 1 }}>
      {results?.map(
        (map, i) =>
          map && (
            <Grid item md={4} sm={6} xs={12} key={i}>
              <CardComponent
                item={map}
                sx={{
                  m: 1,
                  height: (theme) => `calc(100% - ${theme.spacing(2)})`,
                }}
              />
            </Grid>
          )
      )}
    </Grid>
  );
}

export default function ResultDisplay({
  query,
  entityName,
  entityNamePlural,
  max_displayed_count,
  CardComponent,
  defaultExpanded = true,
  addOn,
}) {
  const { data, error, isFetching } = query;
  const results = Array.isArray(data) ? data : data?.results || [];
  const total_count = data?.count;
  const displayed_result_count = Math.min(
    results?.length,
    max_displayed_count || results?.length
  );
  const total_result_count = total_count || results.length || 0;
  const remaining_result_count = total_result_count - displayed_result_count;
  return (
    <Accordion
      variant="outlined"
      disableGutters
      sx={{
        mb: 2,
        "&.MuiAccordion-root:before": {
          display: "none",
        },
        "&.Mui-disabled": { bgcolor: "common.white" },
      }}
      defaultExpanded={defaultExpanded}
    >
      <ResultSummary
        entityName={entityName}
        entityNamePlural={entityNamePlural || `${entityName}s`}
        count={total_result_count}
        errors={error}
        loading={isFetching}
        addOn={addOn}
      />
      {!isFetching && !!displayed_result_count && (
        <AccordionDetails sx={{ pt: 0 }}>
          {results?.length > 0 && (
            <ResultsList
              results={results?.slice(0, displayed_result_count)}
              CardComponent={CardComponent}
            />
          )}
          {remaining_result_count > 0 && (
            <AdditionalResults
              remaining_result_count={remaining_result_count}
              entityNamePlural={entityNamePlural || `${entityName}s`}
            />
          )}
        </AccordionDetails>
      )}
    </Accordion>
  );
}
